from typing import Optional
from uuid import UUID

from fbsrankings.common import Query


class TeamByIDResult:
    def __init__(self, id_: UUID, name: str) -> None:
        self.id_ = id_
        self.name = name


class TeamByIDQuery(Query[Optional[TeamByIDResult]]):
    def __init__(self, id_: UUID) -> None:
        self.id_ = id_
