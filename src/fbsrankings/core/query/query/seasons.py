from typing import List
from uuid import UUID

from dataclasses import dataclass

from fbsrankings.common import Query


@dataclass(frozen=True)
class SeasonResult:
    id_: UUID
    year: int


@dataclass(frozen=True)
class SeasonsResult:
    seasons: List[SeasonResult]


@dataclass(frozen=True)
class SeasonsQuery(Query[SeasonsResult]):
    pass
