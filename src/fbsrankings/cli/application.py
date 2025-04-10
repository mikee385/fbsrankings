import re
from collections.abc import Iterable
from types import TracebackType
from typing import ContextManager
from typing import Literal
from typing import Optional
from typing import Union
from uuid import uuid4

from communication.bus import CommandBus
from communication.bus import EventBus
from communication.bus import QueryBus
from communication.messages import Error
from communication.messages import Event
from communication.messages import MultipleError
from fbsrankings.cli.error import print_err
from fbsrankings.cli.progress import ProgressBar
from fbsrankings.cli.progress import Spinner
from fbsrankings.messages.command import CalculateRankingsForSeasonCommand
from fbsrankings.messages.command import DropStorageCommand
from fbsrankings.messages.command import ImportSeasonByYearCommand
from fbsrankings.messages.enums import GameStatus
from fbsrankings.messages.error import AffiliationDataValidationError
from fbsrankings.messages.error import FBSGameCountValidationError
from fbsrankings.messages.error import FCSGameCountValidationError
from fbsrankings.messages.error import GameDataValidationError
from fbsrankings.messages.error import PostseasonGameCountValidationError
from fbsrankings.messages.error import SeasonDataValidationError
from fbsrankings.messages.error import TeamDataValidationError
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
from fbsrankings.messages.query import AffiliationCountBySeasonResult
from fbsrankings.messages.query import CanceledGamesQuery
from fbsrankings.messages.query import CanceledGamesResult
from fbsrankings.messages.query import GameByIDQuery
from fbsrankings.messages.query import GameByIDResult
from fbsrankings.messages.query import GameCountBySeasonQuery
from fbsrankings.messages.query import GameCountBySeasonResult
from fbsrankings.messages.query import GameRankingBySeasonWeekQuery
from fbsrankings.messages.query import GameRankingBySeasonWeekResult
from fbsrankings.messages.query import GameRankingBySeasonWeekValue
from fbsrankings.messages.query import GameRankingValueBySeasonWeekResult
from fbsrankings.messages.query import LatestSeasonWeekQuery
from fbsrankings.messages.query import LatestSeasonWeekResult
from fbsrankings.messages.query import PostseasonGameCountBySeasonQuery
from fbsrankings.messages.query import PostseasonGameCountBySeasonResult
from fbsrankings.messages.query import SeasonByIDQuery
from fbsrankings.messages.query import SeasonByIDResult
from fbsrankings.messages.query import SeasonByYearQuery
from fbsrankings.messages.query import SeasonByYearResult
from fbsrankings.messages.query import SeasonByYearValue
from fbsrankings.messages.query import SeasonResult
from fbsrankings.messages.query import SeasonsQuery
from fbsrankings.messages.query import SeasonsResult
from fbsrankings.messages.query import TeamByIDQuery
from fbsrankings.messages.query import TeamByIDResult
from fbsrankings.messages.query import TeamCountBySeasonQuery
from fbsrankings.messages.query import TeamCountBySeasonResult
from fbsrankings.messages.query import TeamRankingBySeasonWeekQuery
from fbsrankings.messages.query import TeamRankingBySeasonWeekResult
from fbsrankings.messages.query import TeamRankingBySeasonWeekValue
from fbsrankings.messages.query import TeamRecordBySeasonWeekQuery
from fbsrankings.messages.query import TeamRecordBySeasonWeekResult
from fbsrankings.messages.query import TeamRecordBySeasonWeekValue
from fbsrankings.messages.query import WeekCountBySeasonQuery
from fbsrankings.messages.query import WeekCountBySeasonResult


class GameUpdateTracker(ContextManager["GameUpdateTracker"]):
    def __init__(self, event_bus: EventBus) -> None:
        self._event_bus = event_bus
        self.updates: dict[str, list[int]] = {}

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
        type_: Optional[type[BaseException]],
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

        self._event_counts_by_season: dict[str, dict[type[Event], int]] = {}
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

        self._note_events: list[GameNotesUpdatedEvent] = []
        self._event_bus.register_handler(GameNotesUpdatedEvent, self._save_notes_event)

        self._errors: list[Error] = []
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
                self._command_bus.send(DropStorageCommand(command_id=str(uuid4())))
            print_err()

        with GameUpdateTracker(self._event_bus) as tracker:
            print_err("Importing season data:")
            for year in ProgressBar(years):
                self._command_bus.send(
                    ImportSeasonByYearCommand(command_id=str(uuid4()), year=year),
                )

            if tracker.updates:
                print_err()
                print_err("Calculating rankings:")
                for season_id in ProgressBar(tracker.updates.keys()):
                    self._command_bus.send(
                        CalculateRankingsForSeasonCommand(
                            command_id=str(uuid4()),
                            season_id=season_id,
                        ),
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

        result = self._query_bus.query(
            LatestSeasonWeekQuery(query_id=str(uuid4())),
            LatestSeasonWeekResult,
        )
        if not result.HasField("latest"):
            raise ValueError("No completed weeks were found")
        latest_season_week = result.latest

        season_id = latest_season_week.season_id
        year = latest_season_week.year
        week = latest_season_week.week if latest_season_week.HasField("week") else None

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
            if game.status == GameStatus.GAME_STATUS_COMPLETED:
                completed_games.append(game)
            elif game.status == GameStatus.GAME_STATUS_SCHEDULED:
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

        result = self._query_bus.query(
            SeasonsQuery(query_id=str(uuid4())),
            SeasonsResult,
        )
        if not result.seasons:
            raise ValueError("No seasons were found")
        self._print_seasons_table(result.seasons[:limit])

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
        self._print_games_table(list(game_ranking.values), team_ranking, limit)

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

    def _save_error(self, error: Error) -> None:
        self._errors.append(error)

    def _print_check(self) -> None:
        limit = 10

        season_result = self._query_bus.query(
            SeasonsQuery(query_id=str(uuid4())),
            SeasonsResult,
        )
        if not season_result.seasons:
            raise ValueError("No seasons were found")
        self._print_seasons_table(season_result.seasons)

        result = self._query_bus.query(
            LatestSeasonWeekQuery(query_id=str(uuid4())),
            LatestSeasonWeekResult,
        )
        if not result.HasField("latest"):
            raise ValueError("No completed weeks were found")
        latest_season_week = result.latest

        season_id = latest_season_week.season_id
        year = latest_season_week.year
        week = latest_season_week.week if latest_season_week.HasField("week") else None

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
                list(game_ranking.values),
                team_ranking,
                limit,
            )

    @staticmethod
    def _parse_seasons(seasons: Iterable[str]) -> list[int]:
        years: list[int] = []
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

    def _parse_season_week(self, season_week: str) -> tuple[int, Optional[int]]:
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
            result = self._query_bus.query(
                LatestSeasonWeekQuery(query_id=str(uuid4())),
                LatestSeasonWeekResult,
            )
            if not result.HasField("latest"):
                raise ValueError("No completed weeks were found")
            latest_season_week = result.latest
            year = latest_season_week.year
            week = (
                latest_season_week.week if latest_season_week.HasField("week") else None
            )
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

    def _get_season(self, year: int) -> SeasonByYearValue:
        result = self._query_bus.query(
            SeasonByYearQuery(query_id=str(uuid4()), year=year),
            SeasonByYearResult,
        )
        if not result.HasField("season"):
            raise ValueError(f"Season not found for {year}")
        return result.season

    def _get_team_record(
        self,
        season_id: str,
        year: int,
        week: Optional[int],
    ) -> TeamRecordBySeasonWeekValue:
        result = self._query_bus.query(
            TeamRecordBySeasonWeekQuery(
                query_id=str(uuid4()),
                season_id=season_id,
                week=week,
            ),
            TeamRecordBySeasonWeekResult,
        )
        if not result.HasField("record"):
            if week is not None:
                raise ValueError(f"Team records not found for {year}, Week {week}")
            raise ValueError(f"Team records not found for {year}")
        return result.record

    def _get_team_ranking(
        self,
        rating_name: str,
        season_id: str,
        year: int,
        week: Optional[int],
    ) -> TeamRankingBySeasonWeekValue:
        result = self._query_bus.query(
            TeamRankingBySeasonWeekQuery(
                query_id=str(uuid4()),
                name=rating_name,
                season_id=season_id,
                week=week,
            ),
            TeamRankingBySeasonWeekResult,
        )
        if not result.HasField("ranking"):
            if week is not None:
                raise ValueError(
                    f"Team rankings not found for {rating_name}, {year}, Week {week}",
                )
            raise ValueError(f"Team rankings not found for {rating_name}, {year}")
        return result.ranking

    def _get_game_ranking(
        self,
        rating_name: str,
        season_id: str,
        year: int,
        week: Optional[int],
    ) -> GameRankingBySeasonWeekValue:
        result = self._query_bus.query(
            GameRankingBySeasonWeekQuery(
                query_id=str(uuid4()),
                name=rating_name,
                season_id=season_id,
                week=week,
            ),
            GameRankingBySeasonWeekResult,
        )
        if not result.HasField("ranking"):
            if week is not None:
                raise ValueError(
                    f"Game rankings not found for {rating_name}, {year}, Week {week}",
                )
            raise ValueError(f"Game rankings not found for {rating_name}, {year}")
        return result.ranking

    @staticmethod
    def _print_table(
        header: list[str],
        alignments: list[str],
        rows: list[list[str]],
    ) -> None:
        num_columns = len(header)
        column_widths = [
            max(len(header[column]), max(len(row[column]) for row in rows))
            for column in range(num_columns)
        ]
        separator = "+" + "+".join("-" * (width + 2) for width in column_widths) + "+"

        print(separator)

        line = "| "
        for column in range(num_columns):
            if alignments[column] == "r":
                line += header[column].rjust(column_widths[column]) + " | "
            elif alignments[column] == "l":
                line += header[column].ljust(column_widths[column]) + " | "
            else:
                line += header[column].center(column_widths[column]) + " | "
        print(line.rstrip())

        print(separator)

        for row in rows:
            line = "| "
            for column in range(num_columns):
                if alignments[column] == "r":
                    line += row[column].rjust(column_widths[column]) + " | "
                elif alignments[column] == "l":
                    line += row[column].ljust(column_widths[column]) + " | "
                else:
                    line += row[column].center(column_widths[column]) + " | "
            print(line.rstrip())

        print(separator)

    def _print_seasons_table(self, seasons: Iterable[SeasonResult]) -> None:
        headers = ["Season", "Weeks", "Teams", "FBS", "FCS", "Games", "Post"]
        alignments = ["c", "c", "c", "c", "c", "c", "c"]
        rows = []

        for season in seasons:
            week_count = self._query_bus.query(
                WeekCountBySeasonQuery(
                    query_id=str(uuid4()),
                    season_id=season.season_id,
                ),
                WeekCountBySeasonResult,
            )
            team_count = self._query_bus.query(
                TeamCountBySeasonQuery(
                    query_id=str(uuid4()),
                    season_id=season.season_id,
                ),
                TeamCountBySeasonResult,
            )
            affiliation_count = self._query_bus.query(
                AffiliationCountBySeasonQuery(
                    query_id=str(uuid4()),
                    season_id=season.season_id,
                ),
                AffiliationCountBySeasonResult,
            )
            game_count = self._query_bus.query(
                GameCountBySeasonQuery(
                    query_id=str(uuid4()),
                    season_id=season.season_id,
                ),
                GameCountBySeasonResult,
            )
            postseason_game_count = self._query_bus.query(
                PostseasonGameCountBySeasonQuery(
                    query_id=str(uuid4()),
                    season_id=season.season_id,
                ),
                PostseasonGameCountBySeasonResult,
            )

            rows.append(
                [
                    str(season.year),
                    str(week_count.count),
                    str(team_count.count),
                    str(affiliation_count.fbs_count),
                    str(affiliation_count.fcs_count),
                    str(game_count.count),
                    str(postseason_game_count.count),
                ],
            )

        print()
        self._print_table(headers, alignments, rows)

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

    def _print_teams_table(
        self,
        record: TeamRecordBySeasonWeekValue,
        ranking: TeamRankingBySeasonWeekValue,
        sos: TeamRankingBySeasonWeekValue,
        limit: Optional[int],
    ) -> None:
        record_map = {v.team_id: v for v in record.values}
        sos_map = {v.team_id: v for v in sos.values}

        headers = ["#", "Team", "W-L", "Val", "SOS_#", "SOS_Val"]
        alignments = ["r", "l", "r", "c", "r", "c"]
        rows = []

        values = list(ranking.values)
        if limit is not None:
            values = values[:limit]

        for ranking_value in values:
            record_value = record_map[ranking_value.team_id]
            sos_value = sos_map[ranking_value.team_id]

            rows.append(
                [
                    str(ranking_value.rank),
                    str(ranking_value.name),
                    f"{record_value.wins}-{record_value.losses}",
                    f"{ranking_value.value:.3f}",
                    str(sos_value.rank),
                    f"{sos_value.value:.3f}",
                ],
            )

        self._print_table(headers, alignments, rows)

    def _print_games_table(
        self,
        game_values: list[GameRankingValueBySeasonWeekResult],
        team_ranking: TeamRankingBySeasonWeekValue,
        limit: Optional[int],
    ) -> None:
        team_map = {v.team_id: v for v in team_ranking.values}

        headers = ["Date", "H#", "Home", "A#", "Away", "Score", "Val"]
        alignments = ["c", "r", "l", "r", "l", "r", "c"]
        rows = []

        if limit is None:
            values = game_values
        else:
            values = game_values[:limit]

        for game in values:
            home_team = team_map[game.home_team_id]
            away_team = team_map[game.away_team_id]

            rows.append(
                [
                    str(game.date.ToDatetime().date()),
                    str(home_team.rank),
                    str(game.home_team_name),
                    str(away_team.rank),
                    str(game.away_team_name),
                    (
                        f"{game.home_team_score}-{game.away_team_score}"
                        if game.HasField("home_team_score")
                        and game.HasField("away_team_score")
                        else ""
                    ),
                    f"{game.value:.3f}",
                ],
            )

        self._print_table(headers, alignments, rows)

    def _print_events(self) -> None:
        print()
        print("Events:")
        if self._event_counts_by_season:
            result = self._query_bus.query(
                SeasonsQuery(query_id=str(uuid4())),
                SeasonsResult,
            )
            if not result.seasons:
                raise ValueError("No seasons were found")
            season_map = {s.season_id: s for s in result.seasons}

            headers = [
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
            alignments = ["c", "c", "c", "c", "c", "c", "c", "c", "c", "c"]
            rows = []

            for season, counts in self._event_counts_by_season.items():
                year = season_map[season].year
                rows.append(
                    [
                        str(year),
                        str(counts.get(AffiliationCreatedEvent, 0)),
                        str(counts.get(GameCreatedEvent, 0)),
                        str(counts.get(GameCompletedEvent, 0)),
                        str(counts.get(GameRescheduledEvent, 0)),
                        str(counts.get(GameCanceledEvent, 0)),
                        str(counts.get(GameNotesUpdatedEvent, 0)),
                        str(counts.get(TeamRecordCalculatedEvent, 0)),
                        str(counts.get(TeamRankingCalculatedEvent, 0)),
                        str(counts.get(GameRankingCalculatedEvent, 0)),
                    ],
                )

            self._print_table(headers, alignments, rows)

        else:
            print("None")

    def _print_canceled_games(self) -> None:
        canceled_games = self._query_bus.query(
            CanceledGamesQuery(query_id=str(uuid4())),
            CanceledGamesResult,
        ).games
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
                result = self._query_bus.query(
                    GameByIDQuery(query_id=str(uuid4()), game_id=event.game_id),
                    GameByIDResult,
                )
                if result.HasField("game"):
                    game = result.game

                    print()
                    print(f"ID: {game.game_id}")
                    print(f"Year {game.year}, Week {game.week}")
                    print(game.date)
                    print(game.season_section)
                    print(f"{game.home_team_name} vs. {game.away_team_name}")
                    if game.HasField("home_team_score") and game.HasField(
                        "away_team_score",
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
        fbs_team_errors: list[FBSGameCountValidationError],
        fcs_team_errors: list[FCSGameCountValidationError],
    ) -> None:
        if fbs_team_errors:
            print()
            print("FBS teams with too few games:")
            print()
            for fbs_error in fbs_team_errors:
                season_result = self._query_bus.query(
                    SeasonByIDQuery(
                        query_id=str(uuid4()),
                        season_id=fbs_error.season_id,
                    ),
                    SeasonByIDResult,
                )
                if not season_result.HasField("season"):
                    raise ValueError(f"Season not found for {fbs_error.season_id}")
                fbs_error_season = season_result.season

                team_result = self._query_bus.query(
                    TeamByIDQuery(query_id=str(uuid4()), team_id=fbs_error.team_id),
                    TeamByIDResult,
                )
                if not team_result.HasField("team"):
                    raise ValueError(f"Team not found for {fbs_error.team_id}")
                fbs_error_team = team_result.team

                print(
                    f"{fbs_error_season.year} {fbs_error_team.name}:"
                    f" {fbs_error.game_count}",
                )

        if fcs_team_errors:
            print()
            print("FCS teams with too many games:")
            print()
            for fcs_error in fcs_team_errors:
                season_result = self._query_bus.query(
                    SeasonByIDQuery(
                        query_id=str(uuid4()),
                        season_id=fcs_error.season_id,
                    ),
                    SeasonByIDResult,
                )
                if not season_result.HasField("season"):
                    raise ValueError(f"Season not found for {fcs_error.season_id}")
                fcs_error_season = season_result.season

                team_result = self._query_bus.query(
                    TeamByIDQuery(query_id=str(uuid4()), team_id=fcs_error.team_id),
                    TeamByIDResult,
                )
                if not team_result.HasField("team"):
                    raise ValueError(f"Team not found for {fcs_error.team_id}")
                fcs_error_team = team_result.team

                print(
                    f"{fcs_error_season.year} {fcs_error_team.name}:"
                    f" {fcs_error.game_count}",
                )

    def _print_game_errors(self, game_errors: list[GameDataValidationError]) -> None:
        if game_errors:
            print()
            print("Game Errors:")
            for error in game_errors:
                result = self._query_bus.query(
                    GameByIDQuery(query_id=str(uuid4()), game_id=error.game_id),
                    GameByIDResult,
                )
                if result.HasField("game"):
                    game = result.game

                    print()
                    print(f"ID: {game.game_id}")
                    print(f"Year {game.year}, Week {game.week}")
                    print(game.date)
                    print(game.season_section)
                    print(f"{game.home_team_name} vs. {game.away_team_name}")
                    if game.HasField("home_team_score") and game.HasField(
                        "away_team_score",
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
    def _print_other_errors(other_errors: list[Error]) -> None:
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
            error = MultipleError(str(uuid4()), self._errors)
            self._errors = []
            raise ValueError(f"{type(error).__name__}: {error.message}")
