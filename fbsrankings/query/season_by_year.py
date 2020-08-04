from typing import Optional
from uuid import UUID

from fbsrankings.common import Query


class SeasonByYearResult(object):
    def __init__(self, id: UUID, year: int) -> None:
        self.id = id
        self.year = year


class SeasonByYearQuery(Query[Optional[SeasonByYearResult]]):
    def __init__(self, year: int) -> None:
        self.year = year
