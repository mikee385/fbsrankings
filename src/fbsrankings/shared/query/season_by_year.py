from typing import Optional
from uuid import UUID

from dataclasses import dataclass

from fbsrankings.shared.messaging import Query


@dataclass(frozen=True)
class SeasonByYearResult:
    id_: UUID
    year: int


@dataclass(frozen=True)
class SeasonByYearQuery(Query[Optional[SeasonByYearResult]]):
    year: int
