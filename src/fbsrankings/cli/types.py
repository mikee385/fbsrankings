import argparse
import os
import re


class FileType:
    def __call__(self, value: str) -> str:
        if os.path.isfile(value):
            return value

        raise argparse.ArgumentTypeError(f"'{value}' must be a valid file path")


class SeasonRangeType:
    def __call__(self, value: str) -> str:
        if value.isdecimal():
            return value
        if re.match(r"[0-9]+-[0-9]+", value):
            return value
        if value.casefold() == "latest".casefold():
            return value
        if value.casefold() == "all".casefold():
            return value

        raise argparse.ArgumentTypeError(
            f"'{value}' must be a single season (e.g. 2018), a range (e.g. 2015-2018),"
            " 'latest', or 'all'",
        )


class SeasonWeekType:
    def __call__(self, value: str) -> str:
        if value.isdecimal():
            return value
        if re.match(r"[0-9]+w[0-9]+", value):
            return value
        if value.casefold() == "latest".casefold():
            return value

        raise argparse.ArgumentTypeError(
            f"'{value}' must be season a single season (e.g. 2018), a specific week"
            " within a season (e.g. 2014w10), or 'latest'",
        )


class NumberOrAllType:
    def __call__(self, value: str) -> str:
        if value.isdecimal():
            return value
        if value.casefold() == "all".casefold():
            return value

        raise argparse.ArgumentTypeError(
            f"'{value}' must be a positive integer or 'all'",
        )