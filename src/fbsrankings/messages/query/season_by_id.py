from typing import Optional
from uuid import UUID

from dataclasses import dataclass

from communication.bus import Query


@dataclass(frozen=True)
class SeasonByIDResult:
    id_: UUID
    year: int


@dataclass(frozen=True)
class SeasonByIDQuery(Query[Optional[SeasonByIDResult]]):
    id_: UUID
