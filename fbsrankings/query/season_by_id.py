from typing import Optional
from uuid import UUID

from fbsrankings.common import Query


class SeasonByIDResult:
    def __init__(self, id: UUID, year: int) -> None:
        self.id = id
        self.year = year


class SeasonByIDQuery(Query[Optional[SeasonByIDResult]]):
    def __init__(self, id: UUID) -> None:
        self.id = id
