from typing import Optional
from uuid import UUID

from fbsrankings.common import Query


class SeasonByIDResult(object):
    def __init__(self, ID: UUID, year: int) -> None:
        self.ID = ID
        self.year = year


class SeasonByIDQuery(Query[Optional[SeasonByIDResult]]):
    def __init__(self, ID: UUID) -> None:
        self.ID = ID
