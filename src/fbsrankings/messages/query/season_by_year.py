from typing import Optional
from uuid import UUID

from dataclasses import dataclass

from communication.bus import Query


@dataclass(frozen=True)
class SeasonByYearResult:
    season_id: UUID
    year: int


@dataclass(frozen=True)
class SeasonByYearQuery(Query[Optional[SeasonByYearResult]]):
    query_id: UUID
    year: int
