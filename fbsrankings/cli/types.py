import argparse
import re


class SeasonRangeType(object):
    def __call__(self, value: str) -> str:
        if value.isdecimal():
            return value
        elif re.match(r"[0-9]+-[0-9]+", value):
            return value
        elif value.casefold() == "latest".casefold():
            return value
        elif value.casefold() == "all".casefold():
            return value
        else:
            raise argparse.ArgumentTypeError(
                f"'{value}' must be a single season (e.g. 2018), a range (e.g. 2015-2018), 'latest', or 'all'"
            )


class SeasonWeekType(object):
    def __call__(self, value: str) -> str:
        if value.isdecimal():
            return value
        elif re.match(r"[0-9]+w[0-9]+", value):
            return value
        elif value.casefold() == "latest".casefold():
            return value
        else:
            raise argparse.ArgumentTypeError(
                f"'{value}' must be season a single season (e.g. 2018), a specific week within a season (e.g. 2014w10), or 'latest'"
            )


class NumberOrAllType(object):
    def __call__(self, value: str) -> str:
        if value.isdecimal():
            return value
        elif value.casefold() == "all".casefold():
            return value
        else:
            raise argparse.ArgumentTypeError(
                f"'{value}' must be a positive integer or 'all'"
            )
