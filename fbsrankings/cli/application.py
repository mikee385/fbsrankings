import json
import re
from pathlib import Path
from types import TracebackType
from typing import cast
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type
from typing import Union
from uuid import UUID

import jsonschema
from prettytable import PrettyTable
from tqdm import tqdm
from typing_extensions import Literal
from typing_extensions import Protocol

from fbsrankings.cli.error import print_err
from fbsrankings.cli.spinner import Spinner
from fbsrankings.command import CalculateRankingsForSeasonCommand
from fbsrankings.command import ImportSeasonByYearCommand
from fbsrankings.common import Event
from fbsrankings.common import EventBus
from fbsrankings.common import EventRecorder
from fbsrankings.domain import FBSGameCountValidationError
from fbsrankings.domain import FCSGameCountValidationError
from fbsrankings.domain import GameDataValidationError
from fbsrankings.domain import GameStatus
from fbsrankings.domain import ValidationError
from fbsrankings.event import AffiliationCreatedEvent
from fbsrankings.event import GameCanceledEvent
from fbsrankings.event import GameCompletedEvent
from fbsrankings.event import GameCreatedEvent
from fbsrankings.event import GameNotesUpdatedEvent
from fbsrankings.event import GameRankingCalculatedEvent
from fbsrankings.event import GameRescheduledEvent
from fbsrankings.event import SeasonCreatedEvent
from fbsrankings.event import TeamCreatedEvent
from fbsrankings.event import TeamRankingCalculatedEvent
from fbsrankings.event import TeamRecordCalculatedEvent
from fbsrankings.query import AffiliationCountBySeasonQuery
from fbsrankings.query import CanceledGamesQuery
from fbsrankings.query import GameByIDQuery
from fbsrankings.query import GameCountBySeasonQuery
from fbsrankings.query import GameRankingBySeasonWeekQuery
from fbsrankings.query import GameRankingBySeasonWeekResult
from fbsrankings.query import GameRankingValueBySeasonWeekResult
from fbsrankings.query import LatestSeasonWeekQuery
from fbsrankings.query import SeasonByIDQuery
from fbsrankings.query import SeasonByYearQuery
from fbsrankings.query import SeasonByYearResult
from fbsrankings.query import SeasonResult
from fbsrankings.query import SeasonsQuery
from fbsrankings.query import TeamByIDQuery
from fbsrankings.query import TeamCountBySeasonQuery
from fbsrankings.query import TeamRankingBySeasonWeekQuery
from fbsrankings.query import TeamRankingBySeasonWeekResult
from fbsrankings.query import TeamRecordBySeasonWeekQuery
from fbsrankings.query import TeamRecordBySeasonWeekResult
from fbsrankings.query import WeekCountBySeasonQuery
from fbsrankings.service import Service


class Application:
    def __init__(self, config_location: str):
        package_dir = Path(__file__).resolve().parent.parent

        if config_location is not None:
            config_path = Path(config_location).resolve()
        else:
            config_path = package_dir / "config.json"
        if not config_path.is_file():
            raise ValueError(f"'{config_path}' must be a valid file path")

        with open(config_path) as config_file:
            config = json.load(config_file)

        schema_path = package_dir / "service" / "schema.json"
        with open(schema_path) as schema_file:
            schema = json.load(schema_file)
        jsonschema.validate(config, schema)

        self._event_bus = EventRecorder(EventBus())
        self._service = Service(config, self._event_bus)

    def import_seasons(self, seasons: Iterable[str], drop: bool, check: bool) -> None:
        years = self._parse_seasons(seasons)

        if drop:
            print_err("Dropping existing data:")
            with Spinner():
                self._service.drop()
            print_err()

        update_tracker = self._UpdateTracker(self._event_bus)

        print_err("Importing season data:")
        for year in tqdm(years):
            self._service.send(ImportSeasonByYearCommand(year))

        if update_tracker.updates:
            print_err()
            print_err("Calculating rankings:")
            for season in tqdm(update_tracker.updates):
                self._service.send(CalculateRankingsForSeasonCommand(season))

        if check:
            self._print_check()

        self._print_events()
        # self._print_canceled_games()
        # self._print_notes()
        self._print_errors()

    def print_latest(self, rating: str, top: str) -> None:
        rating_name = self._parse_rating(rating)
        limit = self._parse_top(top)

        latest_season_week = self._service.query(LatestSeasonWeekQuery())
        if latest_season_week is None:
            raise ValueError("No completed weeks were found")

        season_id = latest_season_week.season_id
        year = latest_season_week.year
        week = latest_season_week.week

        team_record = self._get_team_record(season_id, year, week)
        team_ranking = self._get_team_ranking(rating_name, season_id, year, week)
        team_sos = self._get_team_ranking(
            f"{rating_name} - Strength of Schedule - Total", season_id, year, week,
        )
        game_ranking = self._get_game_ranking(
            f"{rating_name} - Game Strength", season_id, year, week,
        )

        self._print_table_title(year, week, "Teams", team_ranking.name)
        self._print_teams_table(year, week, team_record, team_ranking, team_sos, limit)

        completed_games = []
        scheduled_games = []
        next_week_games = []
        for game in game_ranking.values:
            if game.status == GameStatus.COMPLETED.name:
                completed_games.append(game)
            elif game.status == GameStatus.SCHEDULED.name:
                scheduled_games.append(game)
                if week is not None and game.week == week + 1:
                    next_week_games.append(game)

        if len(next_week_games) > 0:
            self._print_table_title(year, week, "Next Week Games", team_ranking.name)
            self._print_games_table(year, week, next_week_games, team_ranking, limit)

        if len(scheduled_games) > 0:
            self._print_table_title(year, week, "Remaining Games", team_ranking.name)
            self._print_games_table(year, week, scheduled_games, team_ranking, limit)

        if len(completed_games) > 0:
            self._print_table_title(year, week, "Completed Games", team_ranking.name)
            self._print_games_table(year, week, completed_games, team_ranking, limit)

    def print_seasons(self, top: str) -> None:
        limit = self._parse_top(top)

        seasons = self._service.query(SeasonsQuery()).seasons
        self._print_seasons_table(seasons[:limit])

    def print_teams(self, season: str, rating: str, top: str) -> None:
        rating_name = self._parse_rating(rating)
        limit = self._parse_top(top)

        year, week = self._parse_season_week(season)

        season_id = self._get_season(year).id
        record = self._get_team_record(season_id, year, week)
        ranking = self._get_team_ranking(rating_name, season_id, year, week)
        sos = self._get_team_ranking(
            f"{rating_name} - Strength of Schedule - Total", season_id, year, week,
        )

        self._print_table_title(year, week, "Teams", ranking.name)
        self._print_teams_table(year, week, record, ranking, sos, limit)

    def print_games(self, season: str, rating: str, top: str) -> None:
        rating_name = self._parse_rating(rating)
        limit = self._parse_top(top)

        year, week = self._parse_season_week(season)

        season_id = self._get_season(year).id
        team_ranking = self._get_team_ranking(rating_name, season_id, year, week)
        game_ranking = self._get_game_ranking(
            f"{rating_name} - Game Strength", season_id, year, week,
        )

        self._print_table_title(year, week, "Season Games", team_ranking.name)
        self._print_games_table(year, week, game_ranking.values, team_ranking, limit)

    def close(self) -> None:
        self._service.close()

    def __enter__(self) -> "Application":
        self._service.__enter__()
        return self

    def __exit__(
        self,
        type: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self._service.__exit__(type, value, traceback)
        return False

    def _print_check(self) -> None:
        limit = 10

        seasons = self._service.query(SeasonsQuery()).seasons
        self._print_seasons_table(seasons)

        latest_season_week = self._service.query(LatestSeasonWeekQuery())
        if latest_season_week is None:
            raise ValueError("No completed weeks were found")

        season_id = latest_season_week.season_id
        year = latest_season_week.year
        week = latest_season_week.week

        for rating_name in ["Simultaneous Wins", "Colley Matrix", "SRS"]:
            team_record = self._get_team_record(season_id, year, week)
            team_ranking = self._get_team_ranking(rating_name, season_id, year, week)
            team_sos = self._get_team_ranking(
                f"{rating_name} - Strength of Schedule - Total", season_id, year, week,
            )
            game_ranking = self._get_game_ranking(
                f"{rating_name} - Game Strength", season_id, year, week,
            )

            self._print_table_title(year, week, "Teams", team_ranking.name)
            self._print_teams_table(
                year, week, team_record, team_ranking, team_sos, limit,
            )

            self._print_table_title(year, week, "Season Games", team_ranking.name)
            self._print_games_table(
                year, week, game_ranking.values, team_ranking, limit,
            )

    class _UpdateTracker:
        def __init__(self, event_bus: EventBus) -> None:
            self.updates: Dict[UUID, List[int]] = {}

            event_bus.register_handler(GameCreatedEvent, self)
            event_bus.register_handler(GameCompletedEvent, self)
            event_bus.register_handler(GameCanceledEvent, self)

        def __call__(
            self, event: Union[GameCreatedEvent, GameCompletedEvent, GameCanceledEvent],
        ) -> None:
            season = self.updates.get(event.season_id)
            if season is None:
                self.updates[event.season_id] = [event.week]
            elif event.week not in season:
                season.append(event.week)

    def _parse_seasons(self, seasons: Iterable[str]) -> List[int]:
        years: List[int] = []
        for value in seasons:
            if value.isdecimal():
                years.append(int(value))
            elif re.match(r"[0-9]+-[0-9]+", value):
                year_strings = value.split("-")
                start_year = int(year_strings[0])
                end_year = int(year_strings[1])
                years.extend(range(start_year, end_year + 1))
            elif value.casefold() == "latest".casefold():
                years.append(max(self._service.seasons))
            elif value.casefold() == "all".casefold():
                years = self._service.seasons
                break
            else:
                raise ValueError(
                    f"'{value}' must be a single season (e.g. 2018), a range (e.g. 2015-2018), 'latest', or 'all'",
                )

        return years

    def _parse_season_week(self, season_week: str) -> Tuple[int, Optional[int]]:
        year: int
        week: Optional[int]
        if season_week.isdecimal():
            year = int(season_week)
            week = None
        elif re.match(r"[0-9]+w[0-9]+", season_week):
            year_week = season_week.split("w")
            year = int(year_week[0])
            week = int(year_week[1])
        elif season_week.casefold() == "latest".casefold():
            latest_season_week = self._service.query(LatestSeasonWeekQuery())
            if latest_season_week is None:
                raise ValueError("No completed weeks were found")
            year = latest_season_week.year
            week = latest_season_week.week
        else:
            raise ValueError(
                f"'{season_week}' must be season a single season (e.g. 2018), a specific week within a season (e.g. 2014w10), or 'latest'",
            )

        return (year, week)

    def _parse_rating(self, rating: str) -> str:
        if rating.casefold() == "SRS".casefold():
            return "SRS"
        elif rating.casefold() == "colley-matrix".casefold():
            return "Colley Matrix"
        elif rating.casefold() == "simultaneous-wins".casefold():
            return "Simultaneous Wins"
        else:
            raise ValueError(f"Unknown rating type: {rating}")

    def _parse_top(self, top: str) -> Optional[int]:
        if top.isdecimal():
            return int(top)
        elif top.casefold() == "all".casefold():
            return None
        else:
            raise ValueError(f"'{top}' must be a positive integer or 'all'")

    def _get_season(self, year: int) -> SeasonByYearResult:
        season = self._service.query(SeasonByYearQuery(year))
        if season is None:
            raise ValueError(f"Season not found for {year}")
        return season

    def _get_team_record(
        self, season_id: UUID, year: int, week: Optional[int],
    ) -> TeamRecordBySeasonWeekResult:
        team_record = self._service.query(TeamRecordBySeasonWeekQuery(season_id, week))
        if team_record is None:
            if week is not None:
                raise ValueError(f"Team records not found for {year}, Week {week}")
            else:
                raise ValueError(f"Team records not found for {year}")
        return team_record

    def _get_team_ranking(
        self, rating_name: str, season_id: UUID, year: int, week: Optional[int],
    ) -> TeamRankingBySeasonWeekResult:
        team_ranking = self._service.query(
            TeamRankingBySeasonWeekQuery(rating_name, season_id, week),
        )
        if team_ranking is None:
            if week is not None:
                raise ValueError(
                    f"Team rankings not found for {rating_name}, {year}, Week {week}",
                )
            else:
                raise ValueError(f"Team rankings not found for {rating_name}, {year}")
        return team_ranking

    def _get_game_ranking(
        self, rating_name: str, season_id: UUID, year: int, week: Optional[int],
    ) -> GameRankingBySeasonWeekResult:
        game_ranking = self._service.query(
            GameRankingBySeasonWeekQuery(rating_name, season_id, week),
        )
        if game_ranking is None:
            if week is not None:
                raise ValueError(
                    f"Game rankings not found for {rating_name}, {year}, Week {week}",
                )
            else:
                raise ValueError(f"Game rankings not found for {rating_name}, {year}")
        return game_ranking

    def _print_seasons_table(self, seasons: Iterable[SeasonResult]) -> None:
        season_summary_table = PrettyTable()
        season_summary_table.field_names = [
            "Season",
            "Weeks",
            "Teams",
            "FBS",
            "FCS",
            "Games",
        ]

        for season in seasons:
            week_count = self._service.query(WeekCountBySeasonQuery(season.id))
            team_count = self._service.query(TeamCountBySeasonQuery(season.id))
            affiliation_count = self._service.query(
                AffiliationCountBySeasonQuery(season.id),
            )
            game_count = self._service.query(GameCountBySeasonQuery(season.id))

            season_summary_table.add_row(
                [
                    season.year,
                    week_count.count,
                    team_count.count,
                    affiliation_count.fbs_count,
                    affiliation_count.fcs_count,
                    game_count.count,
                ],
            )

        print()
        print(season_summary_table)

    def _print_table_title(
        self, year: int, week: Optional[int], header: str, rating_name: str,
    ) -> None:
        print()
        if week is not None:
            print(f"{year}, Week {week} {header}, {rating_name}:")
        else:
            print(f"{year} {header}, {rating_name}:")

    def _print_teams_table(
        self,
        year: int,
        week: Optional[int],
        record: TeamRecordBySeasonWeekResult,
        ranking: TeamRankingBySeasonWeekResult,
        sos: TeamRankingBySeasonWeekResult,
        limit: Optional[int],
    ) -> None:
        record_map = {v.id: v for v in record.values}
        sos_map = {v.id: v for v in sos.values}

        table = PrettyTable()
        table.field_names = [
            "#",
            "Team",
            "W-L",
            "Val",
            "SOS_#",
            "SOS_Val",
        ]
        table.align["#"] = "r"
        table.align["Team"] = "l"
        table.align["W-L"] = "r"
        table.align["Val"] = "c"
        table.align["SOS_#"] = "r"
        table.align["SOS_Val"] = "c"
        table.float_format = ".3"

        if limit is None:
            values = ranking.values
        else:
            values = ranking.values[:limit]

        for ranking_value in values:
            record_value = record_map[ranking_value.id]
            sos_value = sos_map[ranking_value.id]

            table.add_row(
                [
                    ranking_value.rank,
                    ranking_value.name,
                    f"{record_value.wins}-{record_value.losses}",
                    ranking_value.value,
                    sos_value.rank,
                    sos_value.value,
                ],
            )

        print(table)

    def _print_games_table(
        self,
        year: int,
        week: Optional[int],
        game_values: List[GameRankingValueBySeasonWeekResult],
        team_ranking: TeamRankingBySeasonWeekResult,
        limit: Optional[int],
    ) -> None:
        team_map = {v.id: v for v in team_ranking.values}

        table = PrettyTable()
        table.field_names = [
            "Date",
            "H#",
            "Home",
            "A#",
            "Away",
            "Score",
            "Val",
        ]
        table.align["Date"] = "c"
        table.align["H#"] = "r"
        table.align["Home"] = "l"
        table.align["A#"] = "r"
        table.align["Away"] = "l"
        table.align["Score"] = "r"
        table.align["Val"] = "c"
        table.float_format = ".3"

        if limit is None:
            values = game_values
        else:
            values = game_values[:limit]

        for game in values:
            home_team = team_map[game.home_team_id]
            away_team = team_map[game.away_team_id]

            table.add_row(
                [
                    game.date,
                    home_team.rank,
                    game.home_team_name,
                    away_team.rank,
                    game.away_team_name,
                    f"{game.home_team_score}-{game.away_team_score}"
                    if game.home_team_score is not None
                    and game.away_team_score is not None
                    else "",
                    game.value,
                ],
            )

        print(table)

    def _print_events(self) -> None:
        known_events: List[Type[Event]] = [
            SeasonCreatedEvent,
            TeamCreatedEvent,
            AffiliationCreatedEvent,
            GameCreatedEvent,
            GameRescheduledEvent,
            GameCompletedEvent,
            GameCanceledEvent,
            GameNotesUpdatedEvent,
            TeamRecordCalculatedEvent,
            TeamRankingCalculatedEvent,
            GameRankingCalculatedEvent,
        ]
        events = self._event_bus.events

        print()
        print("Events:")
        if events:
            seasons = self._service.query(SeasonsQuery()).seasons
            season_map = {s.id: s for s in seasons}
            event_counts: Dict[int, Dict[Type[Event], int]] = {}
            other_counts: Dict[Type[Event], int] = {}

            class _SeasonEvent(Protocol):
                season_id: UUID

            for event in events:
                event_type = type(event)
                if event_type not in known_events:
                    other_counts.setdefault(event_type, 0)
                    other_counts[event_type] += 1
                elif hasattr(event, "season_id"):
                    year = season_map[cast(_SeasonEvent, event).season_id].year
                    year_counts = event_counts.setdefault(year, {})
                    year_counts.setdefault(event_type, 0)
                    year_counts[event_type] += 1

            event_table = PrettyTable()
            event_table.field_names = [
                "Year",
                "Tm",
                "GmS",
                "GmC",
                "GmR",
                "GmX",
                "GmN",
                "TRd",
                "TRk",
                "GRk",
            ]
            for year, counts in event_counts.items():
                event_table.add_row(
                    [
                        year,
                        counts.get(AffiliationCreatedEvent, 0),
                        counts.get(GameCreatedEvent, 0),
                        counts.get(GameCompletedEvent, 0),
                        counts.get(GameRescheduledEvent, 0),
                        counts.get(GameCanceledEvent, 0),
                        counts.get(GameNotesUpdatedEvent, 0),
                        counts.get(TeamRecordCalculatedEvent, 0),
                        counts.get(TeamRankingCalculatedEvent, 0),
                        counts.get(GameRankingCalculatedEvent, 0),
                    ],
                )
            print(event_table)

            if other_counts:
                other_table = PrettyTable()
                other_table.field_names = ["Type", "Count"]
                other_table.align["Type"] = "l"
                other_table.align["Count"] = "r"

                for other_type, count in other_counts.items():
                    other_table.add_row([other_type.__name__, count])

                print()
                print("Additional Events:")
                print(other_table)
        else:
            print("None")

    def _print_canceled_games(self) -> None:
        canceled_games = self._service.query(CanceledGamesQuery()).games
        if canceled_games:
            print()
            print("Canceled Games:")
            for game in canceled_games:
                print()
                print(f"ID: {game.id}")
                print(f"Year {game.year}, Week {game.week}")
                print(game.date)
                print(game.season_section)
                print(f"{game.home_team_name} vs. {game.away_team_name}")
                print(game.notes)

    def _print_notes(self) -> None:
        notes_events = [
            e for e in self._event_bus.events if isinstance(e, GameNotesUpdatedEvent)
        ]
        if notes_events:
            print()
            print("Notes:")
            for event in notes_events:
                game = self._service.query(GameByIDQuery(event.id))
                if game is not None:
                    print()
                    print(f"ID: {game.id}")
                    print(f"Year {game.year}, Week {game.week}")
                    print(game.date)
                    print(game.season_section)
                    print(f"{game.home_team_name} vs. {game.away_team_name}")
                    if (
                        game.home_team_score is not None
                        and game.away_team_score is not None
                    ):
                        print(
                            f"{game.status}, {game.home_team_score} to {game.away_team_score}",
                        )
                    else:
                        print(game.status)
                    print(f"Old Notes: {event.old_notes}")
                    print(f"New Notes: {event.notes}")

    def _print_errors(self) -> None:
        fbs_team_errors = []
        fcs_team_errors = []
        game_errors = []
        other_errors = []
        for error in self._service.errors:
            if isinstance(error, FBSGameCountValidationError):
                fbs_team_errors.append(error)
            elif isinstance(error, FCSGameCountValidationError):
                fcs_team_errors.append(error)
            elif isinstance(error, GameDataValidationError):
                game_errors.append(error)
            else:
                other_errors.append(error)

        self._print_team_errors(fbs_team_errors, fcs_team_errors)
        self._print_game_errors(game_errors)
        self._print_other_errors(other_errors)

    def _print_team_errors(
        self,
        fbs_team_errors: List[FBSGameCountValidationError],
        fcs_team_errors: List[FCSGameCountValidationError],
    ) -> None:
        if fbs_team_errors:
            print()
            print("FBS teams with too few games:")
            print()
            for fbs_error in fbs_team_errors:
                fbs_error_season = self._service.query(
                    SeasonByIDQuery(fbs_error.season_id),
                )
                fbs_error_team = self._service.query(TeamByIDQuery(fbs_error.team_id))
                if fbs_error_season is not None and fbs_error_team is not None:
                    print(
                        f"{fbs_error_season.year} {fbs_error_team.name}: {fbs_error.game_count}",
                    )

        if fcs_team_errors:
            print()
            print("FCS teams with too many games:")
            print()
            for fcs_error in fcs_team_errors:
                fcs_error_season = self._service.query(
                    SeasonByIDQuery(fcs_error.season_id),
                )
                fcs_error_team = self._service.query(TeamByIDQuery(fcs_error.team_id))
                if fcs_error_season is not None and fcs_error_team is not None:
                    print(
                        f"{fcs_error_season.year} {fcs_error_team.name}: {fcs_error.game_count}",
                    )

    def _print_game_errors(self, game_errors: List[GameDataValidationError]) -> None:
        if game_errors:
            print()
            print("Game Errors:")
            for error in game_errors:
                game = self._service.query(GameByIDQuery(error.game_id))
                if game is not None:
                    print()
                    print(f"ID: {game.id}")
                    print(f"Year {game.year}, Week {game.week}")
                    print(game.date)
                    print(game.season_section)
                    print(f"{game.home_team_name} vs. {game.away_team_name}")
                    if (
                        game.home_team_score is not None
                        and game.away_team_score is not None
                    ):
                        print(
                            f"{game.status}, {game.home_team_score} to {game.away_team_score}",
                        )
                    else:
                        print(game.status)
                    print(game.notes)
                    print(
                        f"For {error.attribute_name}, expected: {error.expected_value}, found: {error.attribute_value}",
                    )

    def _print_other_errors(self, other_errors: List[ValidationError]) -> None:
        if other_errors:
            print()
            print("Other Errors:")
            print()
            for error in other_errors:
                print(error)
