from uuid import UUID

from dataclasses import dataclass

from communication.bus import Query


@dataclass(frozen=True)
class PostseasonGameCountBySeasonResult:
    season_id: UUID
    count: int


@dataclass(frozen=True)
class PostseasonGameCountBySeasonQuery(Query[PostseasonGameCountBySeasonResult]):
    season_id: UUID
