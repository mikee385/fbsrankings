from uuid import UUID

from dataclasses import dataclass

from communication.messages import Query


@dataclass(frozen=True)
class WeekCountBySeasonResult:
    season_id: UUID
    count: int


@dataclass(frozen=True)
class WeekCountBySeasonQuery(Query[WeekCountBySeasonResult]):
    query_id: UUID
    season_id: UUID
