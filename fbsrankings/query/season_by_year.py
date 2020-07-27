from typing import Optional
from uuid import UUID

from fbsrankings.common import Query


class SeasonByYearResult(object):
    def __init__(self, ID: UUID, year: int) -> None:
        self.ID = ID
        self.year = year


class SeasonByYearQuery(Query[Optional[SeasonByYearResult]]):
    def __init__(self, year: int) -> None:
        self.year = year
