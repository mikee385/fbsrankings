from uuid import UUID

from dataclasses import dataclass

from communication.messages import Query


@dataclass(frozen=True)
class TeamCountBySeasonResult:
    season_id: UUID
    count: int


@dataclass(frozen=True)
class TeamCountBySeasonQuery(Query[TeamCountBySeasonResult]):
    query_id: UUID
    season_id: UUID
