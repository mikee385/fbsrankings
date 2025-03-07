from dataclasses import dataclass

from communication.messages import Query


@dataclass(frozen=True)
class WeekCountBySeasonResult:
    season_id: str
    count: int


@dataclass(frozen=True)
class WeekCountBySeasonQuery(Query[WeekCountBySeasonResult]):
    query_id: str
    season_id: str
