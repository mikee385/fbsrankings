import json
from pathlib import Path
from typing import Dict
from typing import Iterable
from typing import List
from typing import Union
from uuid import UUID

import jsonschema  # type: ignore
from prettytable import PrettyTable  # type: ignore
from tqdm import tqdm  # type: ignore

from fbsrankings.application import Application
from fbsrankings.command import CalculateRankingsForSeasonCommand
from fbsrankings.command import ImportSeasonByYearCommand
from fbsrankings.common import EventBus
from fbsrankings.common import EventCounter
from fbsrankings.common import EventRecorder
from fbsrankings.domain import FBSGameCountValidationError
from fbsrankings.domain import FCSGameCountValidationError
from fbsrankings.domain import GameDataValidationError
from fbsrankings.domain import SeasonSection
from fbsrankings.domain import ValidationError
from fbsrankings.event import GameCanceledEvent
from fbsrankings.event import GameCompletedEvent
from fbsrankings.event import GameCreatedEvent
from fbsrankings.event import GameNotesUpdatedEvent
from fbsrankings.query import AffiliationCountBySeasonQuery
from fbsrankings.query import CanceledGamesQuery
from fbsrankings.query import GameByIDQuery
from fbsrankings.query import GameCountBySeasonQuery
from fbsrankings.query import SeasonByIDQuery
from fbsrankings.query import SeasonResult
from fbsrankings.query import SeasonsQuery
from fbsrankings.query import TeamByIDQuery
from fbsrankings.query import TeamCountBySeasonQuery
from fbsrankings.query import TeamRankingBySeasonWeekQuery
from fbsrankings.query import TeamRecordBySeasonWeekQuery


class UpdateTracker(object):
    def __init__(self, event_bus: EventBus) -> None:
        self.updates: Dict[UUID, List[int]] = {}

        event_bus.register_handler(GameCreatedEvent, self)
        event_bus.register_handler(GameCompletedEvent, self)
        event_bus.register_handler(GameCanceledEvent, self)

    def __call__(
        self, event: Union[GameCreatedEvent, GameCompletedEvent, GameCanceledEvent]
    ) -> None:
        if event.season_section == SeasonSection.REGULAR_SEASON.name:
            season = self.updates.get(event.season_ID)
            if season is None:
                self.updates[event.season_ID] = [event.week]
            elif event.week not in season:
                season.append(event.week)


def main() -> int:
    package_dir = Path(__file__).resolve().parent

    config_path = package_dir / "config.json"
    with open(config_path) as config_file:
        config = json.load(config_file)

    schema_path = package_dir / "application" / "schema.json"
    with open(schema_path) as schema_file:
        schema = json.load(schema_file)
    jsonschema.validate(config, schema)

    event_recorder = EventRecorder(EventBus())
    event_bus = EventCounter(event_recorder)

    with Application(config, event_bus) as application:
        update_tracker = UpdateTracker(event_bus)

        print("Importing Season Data:")
        with tqdm(application.seasons) as progress:
            for year in progress:
                application.send(ImportSeasonByYearCommand(year))

        if update_tracker.updates:
            print()
            print("Calculating Rankings:")
            with tqdm(update_tracker.updates) as progress:
                for season in progress:
                    application.send(CalculateRankingsForSeasonCommand(season))

        seasons = application.query(SeasonsQuery()).seasons
        _print_season_summary_table(application, seasons)

        for season in seasons:
            _print_ranking_table(application, season)

        # _print_canceled_games(application)
        # _print_note_events(application, event_recorder)

        _print_event_counts(event_bus)
        _print_errors(application)

        print()

        return 0


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


def _print_ranking_table(application: Application, season: SeasonResult) -> None:
    record = application.query(TeamRecordBySeasonWeekQuery(season.ID, None))
    cm_ranking = application.query(
        TeamRankingBySeasonWeekQuery("Colley Matrix", season.ID, None)
    )
    cm_sos = application.query(
        TeamRankingBySeasonWeekQuery(
            "Colley Matrix - Strength of Schedule - Total", season.ID, None
        )
    )

    if record is not None and cm_ranking is not None and cm_sos is not None:
        record_map = {v.ID: v for v in record.values}
        cm_sos_map = {v.ID: v for v in cm_sos.values}

        ranking_table = PrettyTable()
        ranking_table.field_names = [
            "Rk",
            "Team",
            "W-L",
            "Val",
            "SOS_Rk",
            "SOS_Val",
        ]
        ranking_table.align["Rk"] = "r"
        ranking_table.align["Team"] = "l"
        ranking_table.align["W-L"] = "r"
        ranking_table.align["Val"] = "c"
        ranking_table.align["SOS_Rk"] = "r"
        ranking_table.align["SOS_Val"] = "c"
        ranking_table.float_format = ".3"

        for cm_ranking_value in cm_ranking.values[:10]:
            record_value = record_map[cm_ranking_value.ID]
            cm_sos_value = cm_sos_map[cm_ranking_value.ID]

            ranking_table.add_row(
                [
                    cm_ranking_value.rank,
                    cm_ranking_value.name,
                    f"{record_value.wins}-{record_value.losses}",
                    cm_ranking_value.value,
                    cm_sos_value.rank,
                    cm_sos_value.value,
                ]
            )

        print()
        print(f"{season.year} Top 10 Rankings:")
        print(ranking_table)


def _print_canceled_games(application: Application) -> None:
    canceled_games = application.query(CanceledGamesQuery()).games
    if canceled_games:
        print()
        print("Canceled Games:")
        for canceled_game in canceled_games:
            print()
            print(f"ID: {canceled_game.ID}")
            print(f"Year {canceled_game.year}, Week {canceled_game.week}")
            print(canceled_game.date)
            print(canceled_game.season_section)
            print(f"{canceled_game.home_team_name} vs. {canceled_game.away_team_name}")
            print(canceled_game.notes)


def _print_note_events(application: Application, event_recorder: EventRecorder) -> None:
    notes_events = [
        e for e in event_recorder.events if isinstance(e, GameNotesUpdatedEvent)
    ]
    if notes_events:
        print()
        print("Notes:")
        for notes_event in notes_events:
            notes_game = application.query(GameByIDQuery(notes_event.ID))
            if notes_game is not None:
                print()
                print(f"ID: {notes_game.ID}")
                print(f"Year {notes_game.year}, Week {notes_game.week}")
                print(notes_game.date)
                print(notes_game.season_section)
                print(f"{notes_game.home_team_name} vs. {notes_game.away_team_name}")
                if (
                    notes_game.home_team_score is not None
                    and notes_game.away_team_score is not None
                ):
                    print(
                        f"{notes_game.status}, {notes_game.home_team_score} to {notes_game.away_team_score}"
                    )
                else:
                    print(notes_game.status)
                print(f"Old Notes: {notes_event.old_notes}")
                print(f"New Notes: {notes_event.notes}")


def _print_event_counts(event_bus: EventCounter) -> None:
    print()
    print("Events:")
    if event_bus.counts:
        event_table = PrettyTable()
        event_table.field_names = ["Type", "Count"]
        event_table.align["Type"] = "l"
        event_table.align["Count"] = "r"

        for event_type, count in event_bus.counts.items():
            event_table.add_row([event_type.__name__, count])
        print(event_table)
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
            error_game = application.query(GameByIDQuery(error.game_ID))
            if error_game is not None:
                print()
                print(f"ID: {error_game.ID}")
                print(f"Year {error_game.year}, Week {error_game.week}")
                print(error_game.date)
                print(error_game.season_section)
                print(f"{error_game.home_team_name} vs. {error_game.away_team_name}")
                if (
                    error_game.home_team_score is not None
                    and error_game.away_team_score is not None
                ):
                    print(
                        f"{error_game.status}, {error_game.home_team_score} to {error_game.away_team_score}"
                    )
                else:
                    print(error_game.status)
                print(error_game.notes)
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
