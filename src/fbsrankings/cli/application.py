import re
from types import TracebackType
from typing import ContextManager
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type
from typing import Union
from uuid import UUID
from uuid import uuid4

from prettytable import PrettyTable
from tqdm import tqdm
from typing_extensions import Literal

from communication.bus import CommandBus
from communication.bus import EventBus
from communication.bus import QueryBus
from communication.messages import Event
from fbsrankings.cli.error import print_err
from fbsrankings.cli.spinner import Spinner
from fbsrankings.messages.command import CalculateRankingsForSeasonCommand
from fbsrankings.messages.command import DropStorageCommand
from fbsrankings.messages.command import ImportSeasonByYearCommand
from fbsrankings.messages.enums import GameStatus
from fbsrankings.messages.error import AffiliationDataValidationError
from fbsrankings.messages.error import FBSGameCountValidationError
from fbsrankings.messages.error import FCSGameCountValidationError
from fbsrankings.messages.error import GameDataValidationError
from fbsrankings.messages.error import MultipleValidationError
from fbsrankings.messages.error import PostseasonGameCountValidationError
from fbsrankings.messages.error import SeasonDataValidationError
from fbsrankings.messages.error import TeamDataValidationError
from fbsrankings.messages.error import ValidationError
from fbsrankings.messages.event import AffiliationCreatedEvent
from fbsrankings.messages.event import GameCanceledEvent
from fbsrankings.messages.event import GameCompletedEvent
from fbsrankings.messages.event import GameCreatedEvent
from fbsrankings.messages.event import GameNotesUpdatedEvent
from fbsrankings.messages.event import GameRankingCalculatedEvent
from fbsrankings.messages.event import GameRescheduledEvent
from fbsrankings.messages.event import TeamRankingCalculatedEvent
from fbsrankings.messages.event import TeamRecordCalculatedEvent
from fbsrankings.messages.query import AffiliationCountBySeasonQuery
from fbsrankings.messages.query import CanceledGamesQuery
from fbsrankings.messages.query import GameByIDQuery
from fbsrankings.messages.query import GameCountBySeasonQuery
from fbsrankings.messages.query import GameRankingBySeasonWeekQuery
from fbsrankings.messages.query import GameRankingBySeasonWeekResult
from fbsrankings.messages.query import GameRankingValueBySeasonWeekResult
from fbsrankings.messages.query import LatestSeasonWeekQuery
from fbsrankings.messages.query import PostseasonGameCountBySeasonQuery
from fbsrankings.messages.query import SeasonByIDQuery
from fbsrankings.messages.query import SeasonByYearQuery
from fbsrankings.messages.query import SeasonByYearResult
from fbsrankings.messages.query import SeasonResult
from fbsrankings.messages.query import SeasonsQuery
from fbsrankings.messages.query import TeamByIDQuery
from fbsrankings.messages.query import TeamCountBySeasonQuery
from fbsrankings.messages.query import TeamRankingBySeasonWeekQuery
from fbsrankings.messages.query import TeamRankingBySeasonWeekResult
from fbsrankings.messages.query import TeamRecordBySeasonWeekQuery
from fbsrankings.messages.query import TeamRecordBySeasonWeekResult
from fbsrankings.messages.query import WeekCountBySeasonQuery


class GameUpdateTracker(ContextManager["GameUpdateTracker"]):
    def __init__(self, event_bus: EventBus) -> None:
        self._event_bus = event_bus
        self.updates: Dict[UUID, List[int]] = {}

        self._event_bus.register_handler(GameCreatedEvent, self)
        self._event_bus.register_handler(GameCompletedEvent, self)
        self._event_bus.register_handler(GameCanceledEvent, self)

    def close(self) -> None:
        self._event_bus.unregister_handler(GameCreatedEvent, self)
        self._event_bus.unregister_handler(GameCompletedEvent, self)
        self._event_bus.unregister_handler(GameCanceledEvent, self)

    def __call__(
        self,
        event: Union[GameCreatedEvent, GameCompletedEvent, GameCanceledEvent],
    ) -> None:
        season = self.updates.get(event.season_id)
        if season is None:
            self.updates[event.season_id] = [event.week]
        elif event.week not in season:
            season.append(event.week)

    def __enter__(self) -> "GameUpdateTracker":
        return self

    def __exit__(
        self,
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        return False


class Application:
    def __init__(
        self,
        command_bus: CommandBus,
        query_bus: QueryBus,
        event_bus: EventBus,
    ) -> None:
        self._command_bus = command_bus
        self._query_bus = query_bus
        self._event_bus = event_bus

        self._event_counts_by_season: Dict[UUID, Dict[Type[Event], int]] = {}
        self._event_bus.register_handler(
            AffiliationCreatedEvent,
            self._save_season_event,
        )
        self._event_bus.register_handler(GameCreatedEvent, self._save_season_event)
        self._event_bus.register_handler(GameRescheduledEvent, self._save_season_event)
        self._event_bus.register_handler(GameCanceledEvent, self._save_season_event)
        self._event_bus.register_handler(GameCompletedEvent, self._save_season_event)
        self._event_bus.register_handler(GameNotesUpdatedEvent, self._save_season_event)
        self._event_bus.register_handler(
            TeamRecordCalculatedEvent,
            self._save_season_event,
        )
        self._event_bus.register_handler(
            TeamRankingCalculatedEvent,
            self._save_season_event,
        )
        self._event_bus.register_handler(
            GameRankingCalculatedEvent,
            self._save_season_event,
        )

        self._note_events: List[GameNotesUpdatedEvent] = []
        self._event_bus.register_handler(GameNotesUpdatedEvent, self._save_notes_event)

        self._errors: List[ValidationError] = []
        self._event_bus.register_handler(MultipleValidationError, self._save_error)
        self._event_bus.register_handler(SeasonDataValidationError, self._save_error)
        self._event_bus.register_handler(TeamDataValidationError, self._save_error)
        self._event_bus.register_handler(
            AffiliationDataValidationError,
            self._save_error,
        )
        self._event_bus.register_handler(GameDataValidationError, self._save_error)
        self._event_bus.register_handler(FBSGameCountValidationError, self._save_error)
        self._event_bus.register_handler(FCSGameCountValidationError, self._save_error)
        self._event_bus.register_handler(
            PostseasonGameCountValidationError,
            self._save_error,
        )

    def import_seasons(self, seasons: Iterable[str], drop: bool, check: bool) -> None:
        years = self._parse_seasons(seasons)

        if drop:
            print_err("Dropping existing data:")
            with Spinner():
                self._command_bus.send(DropStorageCommand(uuid4()))
            print_err()

        with GameUpdateTracker(self._event_bus) as tracker:
            print_err("Importing season data:")
            for year in tqdm(years):
                self._command_bus.send(ImportSeasonByYearCommand(uuid4(), year))

            if tracker.updates:
                print_err()
                print_err("Calculating rankings:")
                for season in tqdm(tracker.updates):
                    self._command_bus.send(
                        CalculateRankingsForSeasonCommand(uuid4(), season),
                    )

        if check:
            self._print_check()

        self._print_events()

        debug = False
        if debug:
            self._print_canceled_games()
            self._print_notes()
            self._raise_errors()
        else:
            self._print_errors()

    def print_latest(self, rating: str, top: str) -> None:
        rating_name = self._parse_rating(rating)
        limit = self._parse_top(top)

        latest_season_week = self._query_bus.query(LatestSeasonWeekQuery(uuid4()))
        if latest_season_week is None:
            raise ValueError("No completed weeks were found")

        season_id = latest_season_week.season_id
        year = latest_season_week.year
        week = latest_season_week.week

        team_record = self._get_team_record(season_id, year, week)
        team_ranking = self._get_team_ranking(rating_name, season_id, year, week)
        team_sos = self._get_team_ranking(
            f"{rating_name} - Strength of Schedule - Total",
            season_id,
            year,
            week,
        )
        game_ranking = self._get_game_ranking(
            f"{rating_name} - Game Strength",
            season_id,
            year,
            week,
        )

        self._print_table_title(year, week, "Teams", team_ranking.name)
        self._print_teams_table(team_record, team_ranking, team_sos, limit)

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
            self._print_games_table(next_week_games, team_ranking, limit)

        if len(scheduled_games) > 0:
            self._print_table_title(year, week, "Remaining Games", team_ranking.name)
            self._print_games_table(scheduled_games, team_ranking, limit)

        if len(completed_games) > 0:
            self._print_table_title(year, week, "Completed Games", team_ranking.name)
            self._print_games_table(completed_games, team_ranking, limit)

    def print_seasons(self, top: str) -> None:
        limit = self._parse_top(top)

        seasons = self._query_bus.query(SeasonsQuery(uuid4())).seasons
        self._print_seasons_table(seasons[:limit])

    def print_teams(self, season: str, rating: str, top: str) -> None:
        rating_name = self._parse_rating(rating)
        limit = self._parse_top(top)

        year, week = self._parse_season_week(season)

        season_id = self._get_season(year).season_id
        record = self._get_team_record(season_id, year, week)
        ranking = self._get_team_ranking(rating_name, season_id, year, week)
        sos = self._get_team_ranking(
            f"{rating_name} - Strength of Schedule - Total",
            season_id,
            year,
            week,
        )

        self._print_table_title(year, week, "Teams", ranking.name)
        self._print_teams_table(record, ranking, sos, limit)

    def print_games(self, season: str, rating: str, top: str) -> None:
        rating_name = self._parse_rating(rating)
        limit = self._parse_top(top)

        year, week = self._parse_season_week(season)

        season_id = self._get_season(year).season_id
        team_ranking = self._get_team_ranking(rating_name, season_id, year, week)
        game_ranking = self._get_game_ranking(
            f"{rating_name} - Game Strength",
            season_id,
            year,
            week,
        )

        self._print_table_title(year, week, "Season Games", team_ranking.name)
        self._print_games_table(game_ranking.values, team_ranking, limit)

    def _save_season_event(
        self,
        event: Union[
            AffiliationCreatedEvent,
            GameCreatedEvent,
            GameRescheduledEvent,
            GameCanceledEvent,
            GameCompletedEvent,
            GameNotesUpdatedEvent,
            TeamRecordCalculatedEvent,
            TeamRankingCalculatedEvent,
            GameRankingCalculatedEvent,
        ],
    ) -> None:
        event_type = type(event)
        season_event_counts = self._event_counts_by_season.setdefault(
            event.season_id,
            {},
        )
        season_event_counts.setdefault(event_type, 0)
        season_event_counts[event_type] += 1

    def _save_notes_event(self, event: GameNotesUpdatedEvent) -> None:
        self._note_events.append(event)

    def _save_error(self, error: ValidationError) -> None:
        self._errors.append(error)

    def _print_check(self) -> None:
        limit = 10

        seasons = self._query_bus.query(SeasonsQuery(uuid4())).seasons
        self._print_seasons_table(seasons)

        latest_season_week = self._query_bus.query(LatestSeasonWeekQuery(uuid4()))
        if latest_season_week is None:
            raise ValueError("No completed weeks were found")

        season_id = latest_season_week.season_id
        year = latest_season_week.year
        week = latest_season_week.week

        for rating_name in ["Simultaneous Wins", "Colley Matrix", "SRS"]:
            team_record = self._get_team_record(season_id, year, week)
            team_ranking = self._get_team_ranking(rating_name, season_id, year, week)
            team_sos = self._get_team_ranking(
                f"{rating_name} - Strength of Schedule - Total",
                season_id,
                year,
                week,
            )
            game_ranking = self._get_game_ranking(
                f"{rating_name} - Game Strength",
                season_id,
                year,
                week,
            )

            self._print_table_title(year, week, "Teams", team_ranking.name)
            self._print_teams_table(
                team_record,
                team_ranking,
                team_sos,
                limit,
            )

            self._print_table_title(year, week, "Season Games", team_ranking.name)
            self._print_games_table(
                game_ranking.values,
                team_ranking,
                limit,
            )

    @staticmethod
    def _parse_seasons(seasons: Iterable[str]) -> List[int]:
        years: List[int] = []
        for value in seasons:
            if value.isdecimal():
                years.append(int(value))
            elif re.match(r"[0-9]+-[0-9]+", value):
                year_strings = value.split("-")
                start_year = int(year_strings[0])
                end_year = int(year_strings[1])
                years.extend(range(start_year, end_year + 1))
            else:
                raise ValueError(
                    f"'{value}' must be a single season (e.g. 2018) or a range"
                    " (e.g. 2015-2018)",
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
            latest_season_week = self._query_bus.query(LatestSeasonWeekQuery(uuid4()))
            if latest_season_week is None:
                raise ValueError("No completed weeks were found")
            year = latest_season_week.year
            week = latest_season_week.week
        else:
            raise ValueError(
                f"'{season_week}' must be season a single season (e.g. 2018), a"
                " specific week within a season (e.g. 2014w10), or 'latest'",
            )

        return (year, week)

    @staticmethod
    def _parse_rating(rating: str) -> str:
        if rating.casefold() == "SRS".casefold():
            return "SRS"
        if rating.casefold() == "colley-matrix".casefold():
            return "Colley Matrix"
        if rating.casefold() == "simultaneous-wins".casefold():
            return "Simultaneous Wins"

        raise ValueError(f"Unknown rating type: {rating}")

    @staticmethod
    def _parse_top(top: str) -> Optional[int]:
        if top.isdecimal():
            return int(top)
        if top.casefold() == "all".casefold():
            return None

        raise ValueError(f"'{top}' must be a positive integer or 'all'")

    def _get_season(self, year: int) -> SeasonByYearResult:
        season = self._query_bus.query(SeasonByYearQuery(uuid4(), year))
        if season is None:
            raise ValueError(f"Season not found for {year}")
        return season

    def _get_team_record(
        self,
        season_id: UUID,
        year: int,
        week: Optional[int],
    ) -> TeamRecordBySeasonWeekResult:
        team_record = self._query_bus.query(
            TeamRecordBySeasonWeekQuery(uuid4(), season_id, week),
        )
        if team_record is None:
            if week is not None:
                raise ValueError(f"Team records not found for {year}, Week {week}")
            raise ValueError(f"Team records not found for {year}")
        return team_record

    def _get_team_ranking(
        self,
        rating_name: str,
        season_id: UUID,
        year: int,
        week: Optional[int],
    ) -> TeamRankingBySeasonWeekResult:
        team_ranking = self._query_bus.query(
            TeamRankingBySeasonWeekQuery(uuid4(), rating_name, season_id, week),
        )
        if team_ranking is None:
            if week is not None:
                raise ValueError(
                    f"Team rankings not found for {rating_name}, {year}, Week {week}",
                )
            raise ValueError(f"Team rankings not found for {rating_name}, {year}")
        return team_ranking

    def _get_game_ranking(
        self,
        rating_name: str,
        season_id: UUID,
        year: int,
        week: Optional[int],
    ) -> GameRankingBySeasonWeekResult:
        game_ranking = self._query_bus.query(
            GameRankingBySeasonWeekQuery(uuid4(), rating_name, season_id, week),
        )
        if game_ranking is None:
            if week is not None:
                raise ValueError(
                    f"Game rankings not found for {rating_name}, {year}, Week {week}",
                )
            raise ValueError(f"Game rankings not found for {rating_name}, {year}")
        return game_ranking

    def _print_seasons_table(self, seasons: Iterable[SeasonResult]) -> None:
        season_summary_table = PrettyTable(
            field_names=["Season", "Weeks", "Teams", "FBS", "FCS", "Games", "Post"],
        )

        for season in seasons:
            week_count = self._query_bus.query(
                WeekCountBySeasonQuery(uuid4(), season.season_id),
            )
            team_count = self._query_bus.query(
                TeamCountBySeasonQuery(uuid4(), season.season_id),
            )
            affiliation_count = self._query_bus.query(
                AffiliationCountBySeasonQuery(uuid4(), season.season_id),
            )
            game_count = self._query_bus.query(
                GameCountBySeasonQuery(uuid4(), season.season_id),
            )
            postseason_game_count = self._query_bus.query(
                PostseasonGameCountBySeasonQuery(uuid4(), season.season_id),
            )

            season_summary_table.add_row(
                [
                    season.year,
                    week_count.count,
                    team_count.count,
                    affiliation_count.fbs_count,
                    affiliation_count.fcs_count,
                    game_count.count,
                    postseason_game_count.count,
                ],
            )

        print()
        print(season_summary_table)

    @staticmethod
    def _print_table_title(
        year: int,
        week: Optional[int],
        header: str,
        rating_name: str,
    ) -> None:
        print()
        if week is not None:
            print(f"{year}, Week {week} {header}, {rating_name}:")
        else:
            print(f"{year} {header}, {rating_name}:")

    @staticmethod
    def _print_teams_table(
        record: TeamRecordBySeasonWeekResult,
        ranking: TeamRankingBySeasonWeekResult,
        sos: TeamRankingBySeasonWeekResult,
        limit: Optional[int],
    ) -> None:
        record_map = {v.team_id: v for v in record.values}
        sos_map = {v.team_id: v for v in sos.values}

        table = PrettyTable(
            field_names=["#", "Team", "W-L", "Val", "SOS_#", "SOS_Val"],
        )
        table.align["#"] = "r"
        table.align["Team"] = "l"
        table.align["W-L"] = "r"
        table.align["Val"] = "c"
        table.align["SOS_#"] = "r"
        table.align["SOS_Val"] = "c"
        table.float_format["Val"] = ".3"
        table.float_format["SOS_Val"] = ".3"

        if limit is None:
            values = ranking.values
        else:
            values = ranking.values[:limit]

        for ranking_value in values:
            record_value = record_map[ranking_value.team_id]
            sos_value = sos_map[ranking_value.team_id]

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

    @staticmethod
    def _print_games_table(
        game_values: List[GameRankingValueBySeasonWeekResult],
        team_ranking: TeamRankingBySeasonWeekResult,
        limit: Optional[int],
    ) -> None:
        team_map = {v.team_id: v for v in team_ranking.values}

        table = PrettyTable(
            field_names=["Date", "H#", "Home", "A#", "Away", "Score", "Val"],
        )
        table.align["Date"] = "c"
        table.align["H#"] = "r"
        table.align["Home"] = "l"
        table.align["A#"] = "r"
        table.align["Away"] = "l"
        table.align["Score"] = "r"
        table.align["Val"] = "c"
        table.float_format["Val"] = ".3"

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
                    (
                        f"{game.home_team_score}-{game.away_team_score}"
                        if game.home_team_score is not None
                        and game.away_team_score is not None
                        else ""
                    ),
                    game.value,
                ],
            )

        print(table)

    def _print_events(self) -> None:
        print()
        print("Events:")
        if self._event_counts_by_season:
            seasons = self._query_bus.query(SeasonsQuery(uuid4())).seasons
            season_map = {s.season_id: s for s in seasons}

            event_table = PrettyTable(
                field_names=[
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
                ],
            )
            for season, counts in self._event_counts_by_season.items():
                year = season_map[season].year
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

        else:
            print("None")

    def _print_canceled_games(self) -> None:
        canceled_games = self._query_bus.query(CanceledGamesQuery(uuid4())).games
        if canceled_games:
            print()
            print("Canceled Games:")
            for game in canceled_games:
                print()
                print(f"ID: {game.game_id}")
                print(f"Year {game.year}, Week {game.week}")
                print(game.date)
                print(game.season_section)
                print(f"{game.home_team_name} vs. {game.away_team_name}")
                print(game.notes)

    def _print_notes(self) -> None:
        if self._note_events:
            print()
            print("Notes:")
            for event in self._note_events:
                game = self._query_bus.query(GameByIDQuery(uuid4(), event.game_id))
                if game is not None:
                    print()
                    print(f"ID: {game.game_id}")
                    print(f"Year {game.year}, Week {game.week}")
                    print(game.date)
                    print(game.season_section)
                    print(f"{game.home_team_name} vs. {game.away_team_name}")
                    if (
                        game.home_team_score is not None
                        and game.away_team_score is not None
                    ):
                        print(
                            f"{game.status}, {game.home_team_score} to"
                            f" {game.away_team_score}",
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
        for error in self._errors:
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
                fbs_error_season = self._query_bus.query(
                    SeasonByIDQuery(uuid4(), fbs_error.season_id),
                )
                fbs_error_team = self._query_bus.query(
                    TeamByIDQuery(uuid4(), fbs_error.team_id),
                )
                if fbs_error_season is not None and fbs_error_team is not None:
                    print(
                        f"{fbs_error_season.year} {fbs_error_team.name}:"
                        f" {fbs_error.game_count}",
                    )

        if fcs_team_errors:
            print()
            print("FCS teams with too many games:")
            print()
            for fcs_error in fcs_team_errors:
                fcs_error_season = self._query_bus.query(
                    SeasonByIDQuery(uuid4(), fcs_error.season_id),
                )
                fcs_error_team = self._query_bus.query(
                    TeamByIDQuery(uuid4(), fcs_error.team_id),
                )
                if fcs_error_season is not None and fcs_error_team is not None:
                    print(
                        f"{fcs_error_season.year} {fcs_error_team.name}:"
                        f" {fcs_error.game_count}",
                    )

    def _print_game_errors(self, game_errors: List[GameDataValidationError]) -> None:
        if game_errors:
            print()
            print("Game Errors:")
            for error in game_errors:
                game = self._query_bus.query(GameByIDQuery(uuid4(), error.game_id))
                if game is not None:
                    print()
                    print(f"ID: {game.game_id}")
                    print(f"Year {game.year}, Week {game.week}")
                    print(game.date)
                    print(game.season_section)
                    print(f"{game.home_team_name} vs. {game.away_team_name}")
                    if (
                        game.home_team_score is not None
                        and game.away_team_score is not None
                    ):
                        print(
                            f"{game.status}, {game.home_team_score} to"
                            f" {game.away_team_score}",
                        )
                    else:
                        print(game.status)
                    print(game.notes)
                    print(f"{type(error).__name__}: {error.message}")
                    print(
                        f"For {error.attribute_name}, expected: {error.expected_value},"
                        f" found: {error.attribute_value}",
                    )

    @staticmethod
    def _print_other_errors(other_errors: List[ValidationError]) -> None:
        if other_errors:
            print()
            print("Other Errors:")
            print()
            for error in other_errors:
                print(f"{type(error).__name__}: {error.message}")

    def _raise_errors(self) -> None:
        if len(self._errors) == 1:
            error = self._errors[0]
            self._errors.clear()
            raise ValueError(f"{type(error).__name__}: {error.message}")
        if len(self._errors) > 1:
            error = MultipleValidationError(uuid4(), self._errors)
            self._errors = []
            raise ValueError(f"{type(error).__name__}: {error.message}")
