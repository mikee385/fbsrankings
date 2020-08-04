from uuid import UUID

from fbsrankings.common import Query


class AffiliationCountBySeasonResult(object):
    def __init__(self, season_id: UUID, fbs_count: int, fcs_count: int) -> None:
        self.season_id = season_id
        self.fbs_count = fbs_count
        self.fcs_count = fcs_count


class AffiliationCountBySeasonQuery(Query[AffiliationCountBySeasonResult]):
    def __init__(self, season_id: UUID) -> None:
        self.season_id = season_id
