from typing import List
from uuid import UUID

from dataclasses import dataclass

from communication.bus import Query


@dataclass(frozen=True)
class SeasonResult:
    season_id: UUID
    year: int


@dataclass(frozen=True)
class SeasonsResult:
    seasons: List[SeasonResult]


@dataclass(frozen=True)
class SeasonsQuery(Query[SeasonsResult]):
    query_id: UUID
