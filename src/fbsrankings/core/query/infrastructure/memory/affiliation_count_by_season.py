from fbsrankings.shared.enums import Subdivision
from fbsrankings.shared.query import AffiliationCountBySeasonQuery
from fbsrankings.shared.query import AffiliationCountBySeasonResult
from fbsrankings.storage.memory import Storage


class AffiliationCountBySeasonQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(
        self,
        query: AffiliationCountBySeasonQuery,
    ) -> AffiliationCountBySeasonResult:
        fbs_count = 0
        fcs_count = 0

        affiliations = self._storage.affiliation.for_season(query.season_id)
        for affiliation in affiliations:
            if affiliation.subdivision == Subdivision.FBS.name:
                fbs_count += 1
            elif affiliation.subdivision == Subdivision.FCS.name:
                fcs_count += 1

        return AffiliationCountBySeasonResult(query.season_id, fbs_count, fcs_count)
