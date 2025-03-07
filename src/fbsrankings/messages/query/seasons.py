from typing import List

from dataclasses import dataclass

from communication.messages import Query


@dataclass(frozen=True)
class SeasonResult:
    season_id: str
    year: int


@dataclass(frozen=True)
class SeasonsResult:
    seasons: List[SeasonResult]


@dataclass(frozen=True)
class SeasonsQuery(Query[SeasonsResult]):
    query_id: str
