from dataclasses import dataclass

from communication.messages import Query


@dataclass(frozen=True)
class GameCountBySeasonResult:
    season_id: str
    count: int


@dataclass(frozen=True)
class GameCountBySeasonQuery(Query[GameCountBySeasonResult]):
    query_id: str
    season_id: str
