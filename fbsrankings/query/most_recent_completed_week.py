from typing import Optional
from uuid import UUID

from fbsrankings.common import Query


class MostRecentCompletedWeekResult(object):
    def __init__(self, season_ID: UUID, year: int, week: int) -> None:
        self.season_ID = season_ID
        self.year = year
        self.week = week


class MostRecentCompletedWeekQuery(Query[Optional[MostRecentCompletedWeekResult]]):
    pass
