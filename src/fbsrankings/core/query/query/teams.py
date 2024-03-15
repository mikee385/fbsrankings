from typing import List
from uuid import UUID

from dataclasses import dataclass

from fbsrankings.common import Query


@dataclass(frozen=True)
class TeamResult:
    id_: UUID
    name: str


@dataclass(frozen=True)
class TeamsResult:
    teams: List[TeamResult]


@dataclass(frozen=True)
class TeamsQuery(Query[TeamsResult]):
    pass
