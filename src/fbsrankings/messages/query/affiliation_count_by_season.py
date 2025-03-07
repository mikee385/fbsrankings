from dataclasses import dataclass

from communication.messages import Query


@dataclass(frozen=True)
class AffiliationCountBySeasonResult:
    season_id: str
    fbs_count: int
    fcs_count: int


@dataclass(frozen=True)
class AffiliationCountBySeasonQuery(Query[AffiliationCountBySeasonResult]):
    query_id: str
    season_id: str
