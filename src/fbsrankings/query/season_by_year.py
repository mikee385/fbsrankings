from typing import Optional
from uuid import UUID

from fbsrankings.common import Query


class SeasonByYearResult:
    def __init__(self, id_: UUID, year: int) -> None:
        self.id_ = id_
        self.year = year


class SeasonByYearQuery(Query[Optional[SeasonByYearResult]]):
    def __init__(self, year: int) -> None:
        self.year = year
