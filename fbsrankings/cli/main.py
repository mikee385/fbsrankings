import argparse

from fbsrankings import __version__
from fbsrankings.cli import core
from fbsrankings.cli.types import NumberOrAllType
from fbsrankings.cli.types import SeasonRangeType
from fbsrankings.cli.types import SeasonWeekType


parser = argparse.ArgumentParser(
    prog="fbsrankings",
    description="Team and game rankings for FBS college football based on data from sportsreference.com.",
    allow_abbrev=False,
)
parser.add_argument("-v", "--version", action="version", version=__version__)
subparsers = parser.add_subparsers()

# IMPORT-------------------------------------

import_parser = subparsers.add_parser(
    "import",
    description="Import team and game data for SEASON from sportsreference.com.",
)
import_parser.add_argument(
    "seasons",
    metavar="SEASON",
    type=SeasonRangeType(),
    nargs="+",
    action="store",
    help="Single season (e.g. 2018), range of seasons (e.g. 2015-2018), 'latest' to import the most recent season, or 'all' to import all available seasons. Multiple seasons and/or ranges can also be provided (e.g. 2010 2012-2014 2016 2018-2020).",
)
import_parser.add_argument(
    "-d",
    "--drop",
    action="store_true",
    help="drop the existing data source before importing the data",
)
import_parser.add_argument(
    "-c",
    "--check",
    action="store_true",
    help="print summary information to check that imported data was saved successfully",
)


def import_seasons(args: argparse.Namespace) -> None:
    core.import_seasons(args.seasons, args.drop, args.check)


import_parser.set_defaults(func=import_seasons)

# PRINT--------------------------------------

print_parser = subparsers.add_parser(
    "print", description="Print seasons, team rankings, or game rankings."
)


def print_results(args: argparse.Namespace) -> None:
    if hasattr(args, "print_func"):
        args.print_func(args)
    else:
        print_parser.print_help()


print_parser.set_defaults(func=print_results)
print_subparsers = print_parser.add_subparsers()

# PRINT LATEST-------------------------------

print_latest_parser = print_subparsers.add_parser(
    "latest",
    description="Print team and game rankings for the most recent completed week.",
)
print_latest_parser.add_argument(
    "-r",
    "--rating",
    type=str.casefold,
    choices=["SRS", "colley-matrix", "simultaneous-wins"],
    default="SRS",
    action="store",
    help="rating calculation to use for rankings",
)
print_latest_parser.add_argument(
    "-t",
    "--top",
    metavar="COUNT",
    type=NumberOrAllType(),
    default="10",
    action="store",
    help="number of teams and games to display, or 'all' to display all teams and games",
)


def print_latest(args: argparse.Namespace) -> None:
    core.print_latest(args.rating, args.top)


print_latest_parser.set_defaults(print_func=print_latest)

# PRINT SEASONS------------------------------

print_seasons_parser = print_subparsers.add_parser(
    "seasons", description="Print a summary of all seasons."
)
print_seasons_parser.add_argument(
    "-t",
    "--top",
    metavar="COUNT",
    type=NumberOrAllType(),
    default="all",
    action="store",
    help="number of seasons to display, or 'all' to display all seasons",
)


def print_seasons(args: argparse.Namespace) -> None:
    core.print_seasons(args.top)


print_seasons_parser.set_defaults(print_func=print_seasons)

# PRINT TEAMS--------------------------------

print_teams_parser = print_subparsers.add_parser(
    "teams", description="Print team rankings for SEASON."
)
print_teams_parser.add_argument(
    "season",
    metavar="SEASON",
    type=SeasonWeekType(),
    action="store",
    help="Single season (e.g. 2018), a specific week within a season (e.g. 2014w10), or 'latest' to print the most recent rankings.",
)
print_teams_parser.add_argument(
    "-r",
    "--rating",
    type=str.casefold,
    choices=["SRS", "colley-matrix", "simultaneous-wins"],
    default="SRS",
    action="store",
    help="rating calculation to use for rankings",
)
print_teams_parser.add_argument(
    "-t",
    "--top",
    metavar="COUNT",
    type=NumberOrAllType(),
    default="10",
    action="store",
    help="number of teams to display, or 'all' to display all teams",
)


def print_teams(args: argparse.Namespace) -> None:
    core.print_teams(args.season, args.rating, args.top)


print_teams_parser.set_defaults(print_func=print_teams)

# PRINT GAMES--------------------------------

print_games_parser = print_subparsers.add_parser(
    "games", description="Print game rankings for SEASON."
)
print_games_parser.add_argument(
    "season",
    metavar="SEASON",
    type=SeasonWeekType(),
    action="store",
    help="Single season (e.g. 2018), a specific week within a season (e.g. 2014w10), or 'latest' to print the most recent rankings.",
)
print_games_parser.add_argument(
    "-r",
    "--rating",
    type=str.casefold,
    choices=["SRS", "colley-matrix", "simultaneous-wins"],
    default="SRS",
    action="store",
    help="rating calculation to use for rankings",
)
print_games_parser.add_argument(
    "-t",
    "--top",
    metavar="COUNT",
    type=NumberOrAllType(),
    default="10",
    action="store",
    help="number of games to display, or 'all' to display all games",
)


def print_games(args: argparse.Namespace) -> None:
    core.print_games(args.season, args.rating, args.top)


print_games_parser.set_defaults(print_func=print_games)

# MAIN---------------------------------------


def main() -> None:
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
