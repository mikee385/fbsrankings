import argparse

from fbsrankings import __version__
from fbsrankings.cli import core
from fbsrankings.cli.types import NumberOrAllType
from fbsrankings.cli.types import SeasonRangeType
from fbsrankings.cli.types import SeasonWeekType
    

def import_seasons(args: argparse.Namespace) -> None:
    core.import_seasons(args.seasons, args.drop)
    

def print_rankings(args: argparse.Namespace) -> None:
    core.print_rankings(args.season, args.display, args.rating, args.top)
    
parser = argparse.ArgumentParser(prog="fbsrankings", description="Team and game rankings for FBS college football based on data from sportsreference.com.")
parser.add_argument('--version', action='version', version=__version__)
subparsers = parser.add_subparsers()

import_parser = subparsers.add_parser('import', description="Import team and game data for SEASON from sportsreference.com.")
import_parser.add_argument('seasons', metavar="SEASON", type=SeasonRangeType(), nargs="+", action='store', help="Single season (e.g. 2018), range of seasons (e.g. 2015-2018), 'latest' to import the most recent season, or 'all' to import all available seasons. Multiple seasons and/or ranges can also be provided (e.g. 2010 2012-2014 2016 2018-2020).")
import_parser.add_argument('--drop', action='store_true', help="Drop the existing data source before importing the data")
import_parser.set_defaults(func=import_seasons)

print_parser = subparsers.add_parser('print', description="Print team or game rankings for SEASON.")
print_parser.add_argument('season', metavar="SEASON", type=SeasonWeekType(), action='store', help="Single season (e.g. 2018), a specific week within a season (e.g. 2014w10), or 'latest' to print the most recent rankings.")
print_parser.add_argument('--display', type=str.casefold, choices=["summary", "teams", "games"], default="summary", action='store', help="Type of information to display")
print_parser.add_argument('--rating', type=str.casefold, choices=["SRS", "colley-matrix", "simultaneous-wins"], default="SRS", action='store', help="Rating calculation to use for rankings")
print_parser.add_argument('--top', metavar="COUNT", type=NumberOrAllType(), default="10", action='store', help="Number of teams/games to display, or 'all' to display all teams/games")
print_parser.set_defaults(func=print_rankings)


def main() -> None:
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()
    
if __name__ == "__main__":
    main()

