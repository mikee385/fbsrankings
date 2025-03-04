from uuid import UUID

from dataclasses import dataclass

from communication.bus import Query


@dataclass(frozen=True)
class GameCountBySeasonResult:
    season_id: UUID
    count: int


@dataclass(frozen=True)
class GameCountBySeasonQuery(Query[GameCountBySeasonResult]):
    season_id: UUID
