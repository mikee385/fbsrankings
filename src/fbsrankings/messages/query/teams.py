from typing import List
from uuid import UUID

from dataclasses import dataclass

from communication.bus import Query


@dataclass(frozen=True)
class TeamResult:
    team_id: UUID
    name: str


@dataclass(frozen=True)
class TeamsResult:
    teams: List[TeamResult]


@dataclass(frozen=True)
class TeamsQuery(Query[TeamsResult]):
    query_id: UUID
