import json
import os
from typing import List

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
from fbsrankings.domain import ValidationError
from fbsrankings.event import GameNotesUpdatedEvent
from fbsrankings.query import AffiliationCountBySeasonQuery
from fbsrankings.query import CanceledGamesQuery
from fbsrankings.query import GameByIDQuery
from fbsrankings.query import GameCountBySeasonQuery
from fbsrankings.query import SeasonByIDQuery
from fbsrankings.query import SeasonsQuery
from fbsrankings.query import TeamByIDQuery
from fbsrankings.query import TeamCountBySeasonQuery
from fbsrankings.query import TeamRankingBySeasonWeekQuery


def main() -> int:
    package_dir = os.path.abspath(os.path.dirname(__file__))

    config_path = os.path.join(package_dir, "config.json")
    with open(config_path) as config_file:
        config = json.load(config_file)

    schema_path = os.path.join(package_dir, "application", "schema.json")
    with open(schema_path) as schema_file:
        schema = json.load(schema_file)
    jsonschema.validate(config, schema)

    event_recorder = EventRecorder(EventBus())
    event_bus = EventCounter(event_recorder)

    with Application(config, event_bus) as application:
        with tqdm(application.seasons) as progress:
            for year in progress:
                progress.set_description(f"{year}")

                application.send(ImportSeasonByYearCommand(year))
                application.send(CalculateRankingsForSeasonCommand(year))

                progress.set_description()

        season_summary_table = PrettyTable()
        season_summary_table.field_names = ["Season", "Teams", "FBS", "FCS", "Games"]

        ranking_tables = {}

        seasons = application.query(SeasonsQuery()).seasons
        for season in seasons:
            team_count = application.query(TeamCountBySeasonQuery(season.ID))
            affiliation_count = application.query(
                AffiliationCountBySeasonQuery(season.ID)
            )
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

            cm_ranking = application.query(
                TeamRankingBySeasonWeekQuery("Colley Matrix", season.ID, None)
            )
            sw_ranking = application.query(
                TeamRankingBySeasonWeekQuery("Simultaneous Wins", season.ID, None)
            )

            if cm_ranking is not None and sw_ranking is not None:
                sw_map = {v.ID: v for v in sw_ranking.values}

                ranking_table = PrettyTable()
                ranking_table.field_names = [
                    "Team",
                    "CM_Rk",
                    "CM_Val",
                    "SW_Rk",
                    "SW_Val",
                ]
                ranking_table.float_format = ".3"

                for cm_value in cm_ranking.values[:10]:
                    sw_value = sw_map[cm_value.ID]
                    ranking_table.add_row(
                        [
                            cm_value.name,
                            cm_value.rank,
                            cm_value.value,
                            sw_value.rank,
                            sw_value.value,
                        ]
                    )

                ranking_tables[season.year] = ranking_table

        print()
        print(f"Total Seasons: {len(seasons)}")
        print()
        print(season_summary_table)

        for year, table in ranking_tables.items():
            print()
            print(f"{year} Rankings:")
            print(table)

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
                print(
                    f"{canceled_game.home_team_name} vs. {canceled_game.away_team_name}"
                )
                print(canceled_game.notes)

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

        notes_events = [
            e for e in event_recorder.events if isinstance(e, GameNotesUpdatedEvent)
        ]
        _print_note_events(application, notes_events)

        print()
        print("Events:")
        print()
        if event_bus.counts:
            for event_type, count in event_bus.counts.items():
                print(f"{event_type.__name__}: {count}")
        else:
            print("None")

        print()

        return 0


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


def _print_note_events(
    application: Application, notes_events: List[GameNotesUpdatedEvent]
) -> None:
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
