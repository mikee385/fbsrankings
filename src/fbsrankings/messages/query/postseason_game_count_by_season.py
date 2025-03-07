from dataclasses import dataclass

from communication.messages import Query


@dataclass(frozen=True)
class PostseasonGameCountBySeasonResult:
    season_id: str
    count: int


@dataclass(frozen=True)
class PostseasonGameCountBySeasonQuery(Query[PostseasonGameCountBySeasonResult]):
    query_id: str
    season_id: str
