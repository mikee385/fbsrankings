import argparse
from typing import Optional
from typing import Sequence
from typing import Union

from fbsrankings import __version__
from fbsrankings.cli.application import Application
from fbsrankings.cli.arg_types import FileType
from fbsrankings.cli.arg_types import NumberOrAllType
from fbsrankings.cli.arg_types import SeasonRangeType
from fbsrankings.cli.arg_types import SeasonWeekType
from fbsrankings.cli.environment import Environment
from fbsrankings.cli.error import print_err


# COMMON-------------------------------------

common_parser = argparse.ArgumentParser(
    description="Common parameters used by all commands.",
    add_help=False,
    allow_abbrev=False,
)
common_parser.add_argument("--version", action="version", version=__version__)
common_parser.add_argument(
    "--config",
    metavar="FILE",
    type=FileType(),
    action="store",
    help="location of config file",
)
common_parser.add_argument(
    "--trace",
    action="store_true",
    help="show the full stack trace when an error occurs",
)

# MAIN---------------------------------------

main_parser = argparse.ArgumentParser(
    prog="fbsrankings",
    description="Team and game rankings for FBS college football based on data from"
    " sportsreference.com.",
    parents=[common_parser],
    allow_abbrev=False,
)
subparsers = main_parser.add_subparsers()

# IMPORT-------------------------------------

import_parser = subparsers.add_parser(
    "import",
    description="Import team and game data for SEASON from sportsreference.com.",
    parents=[common_parser],
)
import_parser.add_argument(
    "seasons",
    metavar="SEASON",
    type=SeasonRangeType(),
    nargs="+",
    action="store",
    help="Single season (e.g. 2018) or range of seasons (e.g. 2015-2018)."
    " Multiple seasons and/or ranges can also be provided (e.g. 2010 2012-2014 2016"
    " 2018-2020).",
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
    with Environment(args.config) as env:
        application = Application(env.command_bus, env.query_bus, env.event_bus)
        application.import_seasons(args.seasons, args.drop, args.check)


import_parser.set_defaults(func=import_seasons)

# LATEST-------------------------------------

latest_parser = subparsers.add_parser(
    "latest",
    description="Print team and game rankings for the most recent completed week.",
    parents=[common_parser],
)
latest_parser.add_argument(
    "-r",
    "--rating",
    type=str.casefold,
    choices=["srs", "colley-matrix", "simultaneous-wins"],
    default="srs",
    action="store",
    help="rating calculation to use for rankings",
)
latest_parser.add_argument(
    "-t",
    "--top",
    metavar="COUNT",
    type=NumberOrAllType(),
    default="10",
    action="store",
    help="number of teams and games to display, or 'all' to display all teams and"
    " games",
)


def print_latest(args: argparse.Namespace) -> None:
    with Environment(args.config) as env:
        application = Application(env.command_bus, env.query_bus, env.event_bus)
        application.print_latest(args.rating, args.top)


latest_parser.set_defaults(func=print_latest)

# SEASONS------------------------------------

seasons_parser = subparsers.add_parser(
    "seasons",
    description="Print a summary of all seasons.",
    parents=[common_parser],
)
seasons_parser.add_argument(
    "-t",
    "--top",
    metavar="COUNT",
    type=NumberOrAllType(),
    default="all",
    action="store",
    help="number of seasons to display, or 'all' to display all seasons",
)


def print_seasons(args: argparse.Namespace) -> None:
    with Environment(args.config) as env:
        application = Application(env.command_bus, env.query_bus, env.event_bus)
        application.print_seasons(args.top)


seasons_parser.set_defaults(func=print_seasons)

# TEAMS--------------------------------------

teams_parser = subparsers.add_parser(
    "teams",
    description="Print team rankings for SEASON.",
    parents=[common_parser],
)
teams_parser.add_argument(
    "season",
    metavar="SEASON",
    type=SeasonWeekType(),
    nargs="?",
    default="latest",
    action="store",
    help="Single season (e.g. 2018), a specific week within a season (e.g. 2014w10),"
    " or 'latest' to print the most recent rankings.",
)
teams_parser.add_argument(
    "-r",
    "--rating",
    type=str.casefold,
    choices=["SRS", "colley-matrix", "simultaneous-wins"],
    default="SRS",
    action="store",
    help="rating calculation to use for rankings",
)
teams_parser.add_argument(
    "-t",
    "--top",
    metavar="COUNT",
    type=NumberOrAllType(),
    default="10",
    action="store",
    help="number of teams to display, or 'all' to display all teams",
)


def print_teams(args: argparse.Namespace) -> None:
    with Environment(args.config) as env:
        application = Application(env.command_bus, env.query_bus, env.event_bus)
        application.print_teams(args.season, args.rating, args.top)


teams_parser.set_defaults(func=print_teams)

# GAMES--------------------------------

games_parser = subparsers.add_parser(
    "games",
    description="Print game rankings for SEASON.",
    parents=[common_parser],
)
games_parser.add_argument(
    "season",
    metavar="SEASON",
    type=SeasonWeekType(),
    nargs="?",
    default="latest",
    action="store",
    help="Single season (e.g. 2018), a specific week within a season (e.g. 2014w10),"
    " or 'latest' to print the most recent rankings.",
)
games_parser.add_argument(
    "-r",
    "--rating",
    type=str.casefold,
    choices=["SRS", "colley-matrix", "simultaneous-wins"],
    default="SRS",
    action="store",
    help="rating calculation to use for rankings",
)
games_parser.add_argument(
    "-t",
    "--top",
    metavar="COUNT",
    type=NumberOrAllType(),
    default="10",
    action="store",
    help="number of games to display, or 'all' to display all games",
)


def print_games(args: argparse.Namespace) -> None:
    with Environment(args.config) as env:
        application = Application(env.command_bus, env.query_bus, env.event_bus)
        application.print_games(args.season, args.rating, args.top)


games_parser.set_defaults(func=print_games)

# ENTRY POINT--------------------------------


def main(argv: Optional[Sequence[str]] = None) -> Union[str, int, None]:
    try:
        args = main_parser.parse_args(argv)
    except SystemExit as result:
        return result.code

    if not hasattr(args, "func"):
        main_parser.print_help()
        return 0

    try:
        args.func(args)
    except Exception as error:  # pylint: disable=broad-except # noqa: PIE786
        if args.trace:
            raise
        print_err(f"{type(error).__name__}: {str(error)}")
        return 1

    return 0
