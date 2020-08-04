from typing import List
from uuid import UUID

from fbsrankings.common import Query


class SeasonResult:
    def __init__(self, id: UUID, year: int) -> None:
        self.id = id
        self.year = year


class SeasonsResult:
    def __init__(self, seasons: List[SeasonResult]) -> None:
        self.seasons = seasons


class SeasonsQuery(Query[SeasonsResult]):
    pass
