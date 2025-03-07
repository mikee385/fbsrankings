from typing import Optional

from dataclasses import dataclass

from communication.messages import Query


@dataclass(frozen=True)
class SeasonByYearResult:
    season_id: str
    year: int


@dataclass(frozen=True)
class SeasonByYearQuery(Query[Optional[SeasonByYearResult]]):
    query_id: str
    year: int
