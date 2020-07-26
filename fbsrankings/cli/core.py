import json
import re
import sys
from pathlib import Path
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Union
from uuid import UUID

import jsonschema  # type: ignore
from prettytable import PrettyTable  # type: ignore
from tqdm import tqdm  # type: ignore

from fbsrankings.application import Application
from fbsrankings.cli.tspinner import tspinner
from fbsrankings.command import CalculateRankingsForSeasonCommand
from fbsrankings.command import ImportSeasonByYearCommand
from fbsrankings.common import EventBus
from fbsrankings.common import EventCounter
from fbsrankings.common import EventRecorder
from fbsrankings.domain import FBSGameCountValidationError
from fbsrankings.domain import FCSGameCountValidationError
from fbsrankings.domain import GameDataValidationError
from fbsrankings.domain import GameStatus
from fbsrankings.domain import ValidationError
from fbsrankings.event import GameCanceledEvent
from fbsrankings.event import GameCompletedEvent
from fbsrankings.event import GameCreatedEvent
from fbsrankings.event import GameNotesUpdatedEvent
from fbsrankings.query import AffiliationCountBySeasonQuery
from fbsrankings.query import CanceledGamesQuery
from fbsrankings.query import GameByIDQuery
from fbsrankings.query import GameCountBySeasonQuery
from fbsrankings.query import GameRankingBySeasonWeekQuery
from fbsrankings.query import GameRankingBySeasonWeekResult
from fbsrankings.query import GameRankingValueBySeasonWeekResult
from fbsrankings.query import MostRecentCompletedWeekQuery
from fbsrankings.query import SeasonByIDQuery
from fbsrankings.query import SeasonResult
from fbsrankings.query import SeasonsQuery
from fbsrankings.query import TeamByIDQuery
from fbsrankings.query import TeamCountBySeasonQuery
from fbsrankings.query import TeamRankingBySeasonWeekQuery
from fbsrankings.query import TeamRankingBySeasonWeekResult
from fbsrankings.query import TeamRecordBySeasonWeekQuery
from fbsrankings.query import TeamRecordBySeasonWeekResult


class _UpdateTracker(object):
    def __init__(self, event_bus: EventBus) -> None:
        self.updates: Dict[UUID, List[int]] = {}

        event_bus.register_handler(GameCreatedEvent, self)
        event_bus.register_handler(GameCompletedEvent, self)
        event_bus.register_handler(GameCanceledEvent, self)

    def __call__(
        self, event: Union[GameCreatedEvent, GameCompletedEvent, GameCanceledEvent]
    ) -> None:
        season = self.updates.get(event.season_ID)
        if season is None:
            self.updates[event.season_ID] = [event.week]
        elif event.week not in season:
            season.append(event.week)
            

def print_err(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def _create_application(event_bus: EventBus) -> Application:
    package_dir = Path(__file__).resolve().parent.parent

    config_path = package_dir / "config.json"
    with open(config_path) as config_file:
        config = json.load(config_file)

    schema_path = package_dir / "application" / "schema.json"
    with open(schema_path) as schema_file:
        schema = json.load(schema_file)
    jsonschema.validate(config, schema)

    return Application(config, event_bus)


def import_seasons(seasons: Iterable[str], drop: bool) -> None:
    event_recorder = EventRecorder(EventBus())
    event_counter = EventCounter(event_recorder)

    with _create_application(event_counter) as application:
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
                years.append(max(application.seasons))
            elif value.casefold() == "all".casefold():
                years = application.seasons
                break
            else:
                raise ValueError(
                    f"'{value}' must be a single season (e.g. 2018), a range (e.g. 2015-2018), 'latest', or 'all'"
                )

        update_tracker = _UpdateTracker(event_counter)

        if drop:
            print_err("Dropping existing data...")
            with tspinner():
                application.drop()
            print_err()

        print_err("Importing Season Data:")
        for year in tqdm(years):
            application.send(ImportSeasonByYearCommand(year))

        if update_tracker.updates:
            print_err()
            print_err("Calculating Rankings:")
            for season in tqdm(update_tracker.updates):
                application.send(CalculateRankingsForSeasonCommand(season))

        all_seasons = application.query(SeasonsQuery()).seasons
        _print_season_summary_table(application, all_seasons)

        most_recent_completed_week = application.query(MostRecentCompletedWeekQuery())
        if most_recent_completed_week is not None:
            _print_all_rankings(
                application,
                most_recent_completed_week.season_ID,
                most_recent_completed_week.year,
                most_recent_completed_week.week,
            )

        # _print_note_events(application, event_recorder)

        _print_event_counts(event_counter)
        _print_errors(application)


def print_rankings(season: str, display: str, rating: str, top: str) -> None:
    with _create_application(EventBus()) as application:
        year: int
        week: Optional[int]
        if season.isdecimal():
            year = int(season)
            week = None
        elif re.match(r"[0-9]+w[0-9]+", season):
            year_week = season.split("-")
            year = int(year_week[0])
            week = int(year_week[1])
        elif season.casefold() == "latest".casefold():
            most_recent_completed_week = application.query(
                MostRecentCompletedWeekQuery()
            )
            if most_recent_completed_week is not None:
                year = most_recent_completed_week.year
                week = most_recent_completed_week.week
        else:
            raise ValueError(
                f"'{season}' must be season a single season (e.g. 2018), a specific week within a season (e.g. 2014w10), or 'latest'"
            )

        all_seasons = application.query(SeasonsQuery()).seasons
        seasons_IDs = [item.ID for item in all_seasons if item.year == year]
        if not seasons_IDs:
            raise ValueError(f"Season not found for {year}")
        season_ID = seasons_IDs[0]

        rating_name: str
        if rating.casefold() == "SRS".casefold():
            rating_name = "SRS"
        elif rating.casefold() == "colley-matrix".casefold():
            rating_name = "Colley Matrix"
        elif rating.casefold() == "simultaneous-wins".casefold():
            rating_name = "Simultaneous Wins"
        else:
            raise ValueError(f"Unknown rating type: {rating}")

        limit: Optional[int]
        if top.isdecimal():
            limit = int(top)
        elif top.casefold() == "all".casefold():
            limit = None
        else:
            raise ValueError(f"'{top}' must be a positive integer or 'all'")

        if display == "summary":
            record = application.query(TeamRecordBySeasonWeekQuery(season_ID, week))
            if record is not None:
                _print_ranking_summary(
                    application, rating_name, season_ID, year, week, record, limit
                )

        elif display == "teams":
            record = application.query(TeamRecordBySeasonWeekQuery(season_ID, week))
            ranking = application.query(
                TeamRankingBySeasonWeekQuery(rating_name, season_ID, week)
            )
            sos = application.query(
                TeamRankingBySeasonWeekQuery(
                    f"{rating_name} - Strength of Schedule - Total", season_ID, week
                )
            )
            if record is not None and ranking is not None and sos is not None:
                _print_team_ranking_table(year, week, record, ranking, sos, limit)

        elif display == "games":
            ranking = application.query(
                TeamRankingBySeasonWeekQuery(rating_name, season_ID, week)
            )
            games = application.query(
                GameRankingBySeasonWeekQuery(
                    f"{rating_name} - Game Strength", season_ID, week
                )
            )
            if ranking is not None and games is not None:
                _print_game_rankings(year, week, games, ranking, limit)

        else:
            raise ValueError(f"Unknown display type: {display}")
            

def _print_season_summary_table(
    application: Application, seasons: Iterable[SeasonResult]
) -> None:
    season_summary_table = PrettyTable()
    season_summary_table.field_names = ["Season", "Teams", "FBS", "FCS", "Games"]

    for season in seasons:
        team_count = application.query(TeamCountBySeasonQuery(season.ID))
        affiliation_count = application.query(AffiliationCountBySeasonQuery(season.ID))
        game_count = application.query(GameCountBySeasonQuery(season.ID))

        season_summary_table.add_row(
            [
                season.year,
                team_count.count,
                affiliation_count.fbs_count,
                affiliation_count.fcs_count,
                game_count.count,
            ]
        )

    print()
    print(season_summary_table)


def _print_all_rankings(
    application: Application, season_ID: UUID, year: int, week: int
) -> None:
    record = application.query(TeamRecordBySeasonWeekQuery(season_ID, week))

    if record is not None:
        _print_ranking_summary(
            application, "Simultaneous Wins", season_ID, year, week, record, 10
        )
        _print_ranking_summary(
            application, "Colley Matrix", season_ID, year, week, record, 10
        )
        _print_ranking_summary(application, "SRS", season_ID, year, week, record, 10)


def _print_ranking_summary(
    application: Application,
    ranking_name: str,
    season_ID: UUID,
    year: int,
    week: Optional[int],
    record: TeamRecordBySeasonWeekResult,
    limit: Optional[int],
) -> None:
    ranking = application.query(
        TeamRankingBySeasonWeekQuery(ranking_name, season_ID, week)
    )
    sos = application.query(
        TeamRankingBySeasonWeekQuery(
            f"{ranking_name} - Strength of Schedule - Total", season_ID, week
        )
    )
    if record is not None and ranking is not None and sos is not None:
        _print_team_ranking_table(year, week, record, ranking, sos, limit)

    games = application.query(
        GameRankingBySeasonWeekQuery(f"{ranking_name} - Game Strength", season_ID, week)
    )
    if ranking is not None and games is not None:
        _print_game_rankings(year, week, games, ranking, limit)


def _print_team_ranking_table(
    year: int,
    week: Optional[int],
    record: TeamRecordBySeasonWeekResult,
    ranking: TeamRankingBySeasonWeekResult,
    sos: TeamRankingBySeasonWeekResult,
    limit: Optional[int],
) -> None:
    record_map = {v.ID: v for v in record.values}
    sos_map = {v.ID: v for v in sos.values}

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
        record_value = record_map[ranking_value.ID]
        sos_value = sos_map[ranking_value.ID]

        table.add_row(
            [
                ranking_value.rank,
                ranking_value.name,
                f"{record_value.wins}-{record_value.losses}",
                ranking_value.value,
                sos_value.rank,
                sos_value.value,
            ]
        )

    print()
    if week is not None:
        print(f"{year}, Week {week} Teams, {ranking.name}:")
    else:
        print(f"{year} Teams, {ranking.name}:")
    print(table)
    
    
def _print_game_rankings(
    year: int,
    week: Optional[int],
    game_ranking: GameRankingBySeasonWeekResult,
    team_ranking: TeamRankingBySeasonWeekResult,
    limit: Optional[int],
) -> None:
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
        print()
        if week is not None:
            print(f"{year}, Week {week} Next Week Games, {team_ranking.name}:")
        else:
            print(f"{year} Next Week Games, {team_ranking.name}:")
        _print_game_ranking_table(year, week, next_week_games, team_ranking, limit)
        
    if len(scheduled_games) > 0:
        print()
        if week is not None:
            print(f"{year}, Week {week} Remaining Games, {team_ranking.name}:")
        else:
            print(f"{year} Remaining Games, {team_ranking.name}:")
        _print_game_ranking_table(year, week, scheduled_games, team_ranking, limit)
    
    if len(completed_games) > 0:
        print()
        if week is not None:
            print(f"{year}, Week {week} Completed Games, {team_ranking.name}:")
        else:
            print(f"{year} Completed Games, {team_ranking.name}:")
        _print_game_ranking_table(year, week, completed_games, team_ranking, limit)


def _print_game_ranking_table(
    year: int,
    week: Optional[int],
    game_values: List[GameRankingValueBySeasonWeekResult],
    team_ranking: TeamRankingBySeasonWeekResult,
    limit: Optional[int],
) -> None:
    team_map = {v.ID: v for v in team_ranking.values}

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
        home_team = team_map[game.home_team_ID]
        away_team = team_map[game.away_team_ID]

        table.add_row(
            [
                game.date,
                home_team.rank,
                game.home_team_name,
                away_team.rank,
                game.away_team_name,
                f"{game.home_team_score}-{game.away_team_score}"
                if game.home_team_score is not None and game.away_team_score is not None
                else "",
                game.value,
            ]
        )

    print(table)


def _print_canceled_games(application: Application) -> None:
    canceled_games = application.query(CanceledGamesQuery()).games
    if canceled_games:
        print()
        print("Canceled Games:")
        for game in canceled_games:
            print()
            print(f"ID: {game.ID}")
            print(f"Year {game.year}, Week {game.week}")
            print(game.date)
            print(game.season_section)
            print(f"{game.home_team_name} vs. {game.away_team_name}")
            print(game.notes)


def _print_note_events(application: Application, event_recorder: EventRecorder) -> None:
    notes_events = [
        e for e in event_recorder.events if isinstance(e, GameNotesUpdatedEvent)
    ]
    if notes_events:
        print()
        print("Notes:")
        for event in notes_events:
            game = application.query(GameByIDQuery(event.ID))
            if game is not None:
                print()
                print(f"ID: {game.ID}")
                print(f"Year {game.year}, Week {game.week}")
                print(game.date)
                print(game.season_section)
                print(f"{game.home_team_name} vs. {game.away_team_name}")
                if (
                    game.home_team_score is not None
                    and game.away_team_score is not None
                ):
                    print(
                        f"{game.status}, {game.home_team_score} to {game.away_team_score}"
                    )
                else:
                    print(game.status)
                print(f"Old Notes: {event.old_notes}")
                print(f"New Notes: {event.notes}")


def _print_event_counts(event_bus: EventCounter) -> None:
    print()
    print("Events:")
    if event_bus.counts:
        table = PrettyTable()
        table.field_names = ["Type", "Count"]
        table.align["Type"] = "l"
        table.align["Count"] = "r"

        for event_type, count in event_bus.counts.items():
            table.add_row([event_type.__name__, count])
        print(table)
    else:
        print("None")


def _print_errors(application: Application) -> None:
    fbs_team_errors = []
    fcs_team_errors = []
    game_errors = []
    other_errors = []
    for error in application.errors:
        if isinstance(error, FBSGameCountValidationError):
            fbs_team_errors.append(error)
        elif isinstance(error, FCSGameCountValidationError):
            fcs_team_errors.append(error)
        elif isinstance(error, GameDataValidationError):
            game_errors.append(error)
        else:
            other_errors.append(error)

    _print_team_errors(application, fbs_team_errors, fcs_team_errors)
    _print_game_errors(application, game_errors)
    _print_other_errors(application, other_errors)


def _print_team_errors(
    application: Application,
    fbs_team_errors: List[FBSGameCountValidationError],
    fcs_team_errors: List[FCSGameCountValidationError],
) -> None:
    if fbs_team_errors:
        print()
        print("FBS teams with too few games:")
        print()
        for fbs_error in fbs_team_errors:
            fbs_error_season = application.query(SeasonByIDQuery(fbs_error.season_ID))
            fbs_error_team = application.query(TeamByIDQuery(fbs_error.team_ID))
            if fbs_error_season is not None and fbs_error_team is not None:
                print(
                    f"{fbs_error_season.year} {fbs_error_team.name}: {fbs_error.game_count}"
                )

    if fcs_team_errors:
        print()
        print("FCS teams with too many games:")
        print()
        for fcs_error in fcs_team_errors:
            fcs_error_season = application.query(SeasonByIDQuery(fcs_error.season_ID))
            fcs_error_team = application.query(TeamByIDQuery(fcs_error.team_ID))
            if fcs_error_season is not None and fcs_error_team is not None:
                print(
                    f"{fcs_error_season.year} {fcs_error_team.name}: {fcs_error.game_count}"
                )


def _print_game_errors(
    application: Application, game_errors: List[GameDataValidationError]
) -> None:
    if game_errors:
        print()
        print("Game Errors:")
        for error in game_errors:
            game = application.query(GameByIDQuery(error.game_ID))
            if game is not None:
                print()
                print(f"ID: {game.ID}")
                print(f"Year {game.year}, Week {game.week}")
                print(game.date)
                print(game.season_section)
                print(f"{game.home_team_name} vs. {game.away_team_name}")
                if (
                    game.home_team_score is not None
                    and game.away_team_score is not None
                ):
                    print(
                        f"{game.status}, {game.home_team_score} to {game.away_team_score}"
                    )
                else:
                    print(game.status)
                print(game.notes)
                print(
                    f"For {error.attribute_name}, expected: {error.expected_value}, found: {error.attribute_value}"
                )


def _print_other_errors(
    application: Application, other_errors: List[ValidationError]
) -> None:
    if other_errors:
        print()
        print("Other Errors:")
        print()
        for error in other_errors:
            print(error)

