import json
import re
from pathlib import Path
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union
from uuid import UUID

import click
import jsonschema  # type: ignore
from prettytable import PrettyTable  # type: ignore
from tqdm import tqdm  # type: ignore

import fbsrankings
from fbsrankings.application import Application
from fbsrankings.cli.types import NumberOrAllType
from fbsrankings.cli.types import SeasonRangeType
from fbsrankings.cli.types import SeasonWeekType
from fbsrankings.command import CalculateRankingsForSeasonCommand
from fbsrankings.command import ImportSeasonByYearCommand
from fbsrankings.common import EventBus
from fbsrankings.common import EventCounter
from fbsrankings.common import EventRecorder
from fbsrankings.domain import FBSGameCountValidationError
from fbsrankings.domain import FCSGameCountValidationError
from fbsrankings.domain import GameDataValidationError
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


@click.group("fbsrankings")
@click.version_option(prog_name="fbsrankings", version=fbsrankings.__version__)
def main() -> None:
    """Team and game rankings for FBS college football based on data from sportsreference.com."""
    pass


@main.command("import")
@click.argument("seasons", type=SeasonRangeType(), nargs=-1, required=True)
def import_seasons(seasons: Tuple[str]) -> None:
    """Import team and game data for SEASON for sportsreference.com.

    SEASON can be a single season (e.g. 2018), a range (e.g. 2015-2018), or 'all' to import all available seasons.
    Multiple seasons and/or ranges can also be provided (e.g. 2010 2012-2014 2016 2018-2020).
    """

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
            elif value.casefold() == "all".casefold():
                years = application.seasons
                break

        update_tracker = _UpdateTracker(event_counter)

        click.echo("Importing Season Data:")
        for year in tqdm(years):
            application.send(ImportSeasonByYearCommand(year))

        if update_tracker.updates:
            click.echo()
            click.echo("Calculating Rankings:")
            for season in tqdm(update_tracker.updates):
                application.send(CalculateRankingsForSeasonCommand(season))

        all_seasons = application.query(SeasonsQuery()).seasons
        _print_season_summaries(application, all_seasons)

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


@main.command("print")
@click.argument("season", type=SeasonWeekType(), nargs=1, required=True)
@click.option(
    "--display",
    type=click.Choice(["summary", "teams", "games"], case_sensitive=False),
    default="summary",
    help="Type of information to display",
)
@click.option(
    "--rating",
    type=click.Choice(
        ["SRS", "colley-matrix", "simultaneous-wins"], case_sensitive=False
    ),
    default="SRS",
    help="Rating calculation to use for rankings",
)
@click.option(
    "--top",
    type=NumberOrAllType(),
    default="10",
    help="Number of teams/games to display, or 'all' to display all teams/games",
)
def print_rankings(season: str, display: str, rating: str, top: str) -> None:
    """Print team or game rankings for SEASON.

    SEASON can be a single season (e.g. 2018), a specific week within a season (e.g. 2014w10), or 'latest' to print the most recent rankings.
    """

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

        all_seasons = application.query(SeasonsQuery()).seasons
        season_ID = next(iter(item.ID for item in all_seasons if item.year == year))

        rating_name: str
        if rating.casefold() == "SRS".casefold():
            rating_name = "SRS"
        elif rating.casefold() == "colley-matrix".casefold():
            rating_name = "Colley Matrix"
        elif rating.casefold() == "simultaneous-wins".casefold():
            rating_name = "Simultaneous Wins"

        limit: Optional[int]
        if top.isdecimal():
            limit = int(top)
        elif top.casefold() == "all".casefold():
            limit = None

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
                _print_game_ranking_table(year, week, games, ranking, limit)


def _print_season_summaries(
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

    click.echo()
    click.echo(season_summary_table)


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
        _print_game_ranking_table(year, week, games, ranking, limit)


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

    click.echo()
    if week is not None:
        if limit is not None:
            click.echo(f"{year}, Week {week} Top {limit} Teams, {ranking.name}:")
        else:
            click.echo(f"{year}, Week {week} Teams, {ranking.name}:")
    else:
        if limit is not None:
            click.echo(f"{year} Top {limit} Teams, {ranking.name}:")
        else:
            click.echo(f"{year} Teams, {ranking.name}:")
    click.echo(table)


def _print_game_ranking_table(
    year: int,
    week: Optional[int],
    game_ranking: GameRankingBySeasonWeekResult,
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
        values = game_ranking.values
    else:
        values = game_ranking.values[:limit]

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

    click.echo()
    if week is not None:
        if limit is not None:
            click.echo(f"{year}, Week {week} Top {limit} Games, {team_ranking.name}:")
        else:
            click.echo(f"{year}, Week {week} Games, {team_ranking.name}:")
    else:
        if limit is not None:
            click.echo(f"{year} Top {limit} Games, {team_ranking.name}:")
        else:
            click.echo(f"{year} Games, {team_ranking.name}:")
    click.echo(table)


def _print_canceled_games(application: Application) -> None:
    canceled_games = application.query(CanceledGamesQuery()).games
    if canceled_games:
        click.echo()
        click.echo("Canceled Games:")
        for game in canceled_games:
            click.echo()
            click.echo(f"ID: {game.ID}")
            click.echo(f"Year {game.year}, Week {game.week}")
            click.echo(game.date)
            click.echo(game.season_section)
            click.echo(f"{game.home_team_name} vs. {game.away_team_name}")
            click.echo(game.notes)


def _print_note_events(application: Application, event_recorder: EventRecorder) -> None:
    notes_events = [
        e for e in event_recorder.events if isinstance(e, GameNotesUpdatedEvent)
    ]
    if notes_events:
        click.echo()
        click.echo("Notes:")
        for event in notes_events:
            game = application.query(GameByIDQuery(event.ID))
            if game is not None:
                click.echo()
                click.echo(f"ID: {game.ID}")
                click.echo(f"Year {game.year}, Week {game.week}")
                click.echo(game.date)
                click.echo(game.season_section)
                click.echo(f"{game.home_team_name} vs. {game.away_team_name}")
                if (
                    game.home_team_score is not None
                    and game.away_team_score is not None
                ):
                    click.echo(
                        f"{game.status}, {game.home_team_score} to {game.away_team_score}"
                    )
                else:
                    click.echo(game.status)
                click.echo(f"Old Notes: {event.old_notes}")
                click.echo(f"New Notes: {event.notes}")


def _print_event_counts(event_bus: EventCounter) -> None:
    click.echo()
    click.echo("Events:")
    if event_bus.counts:
        table = PrettyTable()
        table.field_names = ["Type", "Count"]
        table.align["Type"] = "l"
        table.align["Count"] = "r"

        for event_type, count in event_bus.counts.items():
            table.add_row([event_type.__name__, count])
        click.echo(table)
    else:
        click.echo("None")


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
        click.echo()
        click.echo("FBS teams with too few games:")
        click.echo()
        for fbs_error in fbs_team_errors:
            fbs_error_season = application.query(SeasonByIDQuery(fbs_error.season_ID))
            fbs_error_team = application.query(TeamByIDQuery(fbs_error.team_ID))
            if fbs_error_season is not None and fbs_error_team is not None:
                click.echo(
                    f"{fbs_error_season.year} {fbs_error_team.name}: {fbs_error.game_count}"
                )

    if fcs_team_errors:
        click.echo()
        click.echo("FCS teams with too many games:")
        click.echo()
        for fcs_error in fcs_team_errors:
            fcs_error_season = application.query(SeasonByIDQuery(fcs_error.season_ID))
            fcs_error_team = application.query(TeamByIDQuery(fcs_error.team_ID))
            if fcs_error_season is not None and fcs_error_team is not None:
                click.echo(
                    f"{fcs_error_season.year} {fcs_error_team.name}: {fcs_error.game_count}"
                )


def _print_game_errors(
    application: Application, game_errors: List[GameDataValidationError]
) -> None:
    if game_errors:
        click.echo()
        click.echo("Game Errors:")
        for error in game_errors:
            game = application.query(GameByIDQuery(error.game_ID))
            if game is not None:
                click.echo()
                click.echo(f"ID: {game.ID}")
                click.echo(f"Year {game.year}, Week {game.week}")
                click.echo(game.date)
                click.echo(game.season_section)
                click.echo(f"{game.home_team_name} vs. {game.away_team_name}")
                if (
                    game.home_team_score is not None
                    and game.away_team_score is not None
                ):
                    click.echo(
                        f"{game.status}, {game.home_team_score} to {game.away_team_score}"
                    )
                else:
                    click.echo(game.status)
                click.echo(game.notes)
                click.echo(
                    f"For {error.attribute_name}, expected: {error.expected_value}, found: {error.attribute_value}"
                )


def _print_other_errors(
    application: Application, other_errors: List[ValidationError]
) -> None:
    if other_errors:
        click.echo()
        click.echo("Other Errors:")
        click.echo()
        for error in other_errors:
            click.echo(error)


if __name__ == "__main__":
    main(prog_name="fbsrankings")
