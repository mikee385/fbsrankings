from uuid import UUID

from dataclasses import dataclass

from fbsrankings.shared.messaging import Query


@dataclass(frozen=True)
class AffiliationCountBySeasonResult:
    season_id: UUID
    fbs_count: int
    fcs_count: int


@dataclass(frozen=True)
class AffiliationCountBySeasonQuery(Query[AffiliationCountBySeasonResult]):
    season_id: UUID
