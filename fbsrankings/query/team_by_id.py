from typing import Optional
from uuid import UUID

from fbsrankings.common import Query


class TeamByIDResult(object):
    def __init__(self, id: UUID, name: str) -> None:
        self.id = id
        self.name = name


class TeamByIDQuery(Query[Optional[TeamByIDResult]]):
    def __init__(self, id: UUID) -> None:
        self.id = id
