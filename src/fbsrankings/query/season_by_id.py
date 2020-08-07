from typing import Optional
from uuid import UUID

from fbsrankings.common import Query


class SeasonByIDResult:
    def __init__(self, id_: UUID, year: int) -> None:
        self.id_ = id_
        self.year = year


class SeasonByIDQuery(Query[Optional[SeasonByIDResult]]):
    def __init__(self, id_: UUID) -> None:
        self.id_ = id_
