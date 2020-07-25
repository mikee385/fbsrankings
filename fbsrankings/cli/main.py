from typing import Tuple

import click

from fbsrankings import __version__
from fbsrankings.cli import core
from fbsrankings.cli.types import NumberOrAllType
from fbsrankings.cli.types import SeasonRangeType
from fbsrankings.cli.types import SeasonWeekType


@click.group("fbsrankings")
@click.version_option(prog_name="fbsrankings", version=__version__)
def main() -> None:
    """Team and game rankings for FBS college football based on data from sportsreference.com."""
    pass


@main.command("import")
@click.argument("seasons", type=SeasonRangeType(), nargs=-1, required=True)
@click.option(
    "--drop",
    is_flag=True,
    default=False,
    help="Drop the existing data source before importing the data",
)
def import_seasons(seasons: Tuple[str], drop: bool) -> None:
    """Import team and game data for SEASON for sportsreference.com.

    SEASON can be a single season (e.g. 2018), a range (e.g. 2015-2018), 'latest' to import the most recent season, or 'all' to import all available seasons.
    Multiple seasons and/or ranges can also be provided (e.g. 2010 2012-2014 2016 2018-2020).
    """
    
    core.import_seasons(seasons, drop)


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
    
    core.print_rankings(season, display, rating, top)


if __name__ == "__main__":
    main(prog_name="fbsrankings")

