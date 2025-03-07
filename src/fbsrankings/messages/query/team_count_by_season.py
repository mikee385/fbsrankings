from dataclasses import dataclass

from communication.messages import Query


@dataclass(frozen=True)
class TeamCountBySeasonResult:
    season_id: str
    count: int


@dataclass(frozen=True)
class TeamCountBySeasonQuery(Query[TeamCountBySeasonResult]):
    query_id: str
    season_id: str
