from typing import Optional
from uuid import UUID

from dataclasses import dataclass

from communication.bus import Query


@dataclass(frozen=True)
class TeamByIDResult:
    id_: UUID
    name: str


@dataclass(frozen=True)
class TeamByIDQuery(Query[Optional[TeamByIDResult]]):
    id_: UUID
