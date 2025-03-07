from typing import Optional
from uuid import UUID

from dataclasses import dataclass

from communication.messages import Query


@dataclass(frozen=True)
class TeamByIDResult:
    team_id: UUID
    name: str


@dataclass(frozen=True)
class TeamByIDQuery(Query[Optional[TeamByIDResult]]):
    query_id: UUID
    team_id: UUID
