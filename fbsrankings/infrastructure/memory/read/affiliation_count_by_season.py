from fbsrankings.common import Query, QueryHandler
from fbsrankings.domain import Subdivision
from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.query import AffiliationCountBySeasonQuery, AffiliationCountBySeasonResult


class AffiliationCountBySeasonQueryHandler (QueryHandler):
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def handle(self, query: Query) -> AffiliationCountBySeasonResult:
        if not isinstance(query, AffiliationCountBySeasonQuery):
            raise TypeError('query must be of type AffiliationCountBySeasonQuery')

        fbs_count = 0
        fcs_count = 0
        
        affiliations = self._storage.affiliation.by_season(query.season_ID)
        for affiliation in affiliations:
            if affiliation.subdivision == Subdivision.FBS.name:
                fbs_count += 1
            elif affiliation.subdivision == Subdivision.FCS.name:
                fcs_count += 1
        
        return AffiliationCountBySeasonResult(query.season_ID, fbs_count, fcs_count)
