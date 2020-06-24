from typing import Optional
from uuid import UUID

from fbsrankings.common import Query


class TeamByIDResult(object):
    def __init__(self, ID: UUID, name: str) -> None:
        self.ID = ID
        self.name = name


class TeamByIDQuery(Query[Optional[TeamByIDResult]]):
    def __init__(self, ID: UUID) -> None:
        self.ID = ID
