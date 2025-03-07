from typing import Optional

from dataclasses import dataclass

from communication.messages import Query


@dataclass(frozen=True)
class TeamByIDResult:
    team_id: str
    name: str


@dataclass(frozen=True)
class TeamByIDQuery(Query[Optional[TeamByIDResult]]):
    query_id: str
    team_id: str
