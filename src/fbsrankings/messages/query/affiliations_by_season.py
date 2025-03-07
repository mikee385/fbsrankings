from typing import List

from dataclasses import dataclass

from communication.messages import Query


@dataclass(frozen=True)
class AffiliationBySeasonResult:
    affiliation_id: str
    season_id: str
    year: int
    team_id: str
    team_name: str
    subdivision: str


@dataclass(frozen=True)
class AffiliationsBySeasonResult:
    affiliations: List[AffiliationBySeasonResult]


@dataclass(frozen=True)
class AffiliationsBySeasonQuery(Query[AffiliationsBySeasonResult]):
    query_id: str
    season_id: str
