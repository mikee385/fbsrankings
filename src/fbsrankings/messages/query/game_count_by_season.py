from uuid import UUID

from dataclasses import dataclass

from communication.messages import Query


@dataclass(frozen=True)
class GameCountBySeasonResult:
    season_id: UUID
    count: int


@dataclass(frozen=True)
class GameCountBySeasonQuery(Query[GameCountBySeasonResult]):
    query_id: UUID
    season_id: UUID
