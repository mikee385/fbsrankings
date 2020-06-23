from uuid import UUID

from fbsrankings.common import Query


class AffiliationCountBySeasonQuery(Query):
    def __init__(self, season_ID: UUID) -> None:
        self.season_ID = season_ID


class AffiliationCountBySeasonResult(object):
    def __init__(self, season_ID: UUID, fbs_count: int, fcs_count: int) -> None:
        self.season_ID = season_ID
        self.fbs_count = fbs_count
        self.fcs_count = fcs_count
