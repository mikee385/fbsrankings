from typing import List
from uuid import UUID

from dataclasses import dataclass

from communication.bus import Query


@dataclass(frozen=True)
class AffiliationBySeasonResult:
    id_: UUID
    season_id: UUID
    year: int
    team_id: UUID
    team_name: str
    subdivision: str


@dataclass(frozen=True)
class AffiliationsBySeasonResult:
    affiliations: List[AffiliationBySeasonResult]


@dataclass(frozen=True)
class AffiliationsBySeasonQuery(Query[AffiliationsBySeasonResult]):
    season_id: UUID
