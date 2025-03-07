from typing import List

from dataclasses import dataclass

from communication.messages import Query


@dataclass(frozen=True)
class TeamResult:
    team_id: str
    name: str


@dataclass(frozen=True)
class TeamsResult:
    teams: List[TeamResult]


@dataclass(frozen=True)
class TeamsQuery(Query[TeamsResult]):
    query_id: str
