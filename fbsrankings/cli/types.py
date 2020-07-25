import re
from typing import Optional

import click


class SeasonRangeType(click.ParamType):
    name = "SEASON"

    def convert(
        self,
        value: str,
        param: Optional[click.Parameter],
        ctx: Optional[click.Context],
    ) -> str:
        if value.isdecimal():
            return value
        elif re.match(r"[0-9]+-[0-9]+", value):
            return value
        elif value.casefold() == "latest".casefold():
            return value
        elif value.casefold() == "all".casefold():
            return value
        else:
            self.fail(
                f"'{value}' must be a single season (e.g. 2018), a range (e.g. 2015-2018), 'latest', or 'all'",
                param,
                ctx,
            )


class SeasonWeekType(click.ParamType):
    name = "SEASON-WEEK"

    def convert(
        self,
        value: str,
        param: Optional[click.Parameter],
        ctx: Optional[click.Context],
    ) -> str:
        if value.isdecimal():
            return value
        elif re.match(r"[0-9]+w[0-9]+", value):
            return value
        elif value.casefold() == "latest".casefold():
            return value
        else:
            self.fail(
                f"'{value}' must be season a single season (e.g. 2018), a specific week within a season (e.g. 2014w10), or 'latest'",
                param,
                ctx,
            )


class NumberOrAllType(click.ParamType):
    name = "COUNT"

    def convert(
        self,
        value: str,
        param: Optional[click.Parameter],
        ctx: Optional[click.Context],
    ) -> str:
        if value.isdecimal():
            return value
        elif value.casefold() == "all".casefold():
            return value
        else:
            self.fail(f"'{value}' must be a positive integer or 'all'", param, ctx)
