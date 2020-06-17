from fbsrankings.domain import Subdivision
from fbsrankings.query import AffiliationCountBySeasonResult
from fbsrankings.infrastructure.memory.storage import Storage


class AffiliationCountBySeasonQueryHandler (object):
    def __init__(self, storage):
        if not isinstance(storage, Storage):
            raise TypeError('storage must be of type Storage')
        self._storage = storage

    def handle(self, query):
        fbs_count = 0
        fcs_count = 0
        
        affiliations = self._storage.affiliation.find_by_season(query.season_ID)
        for affiliation in affiliations:
            if affiliation.subdivision == Subdivision.FBS:
                fbs_count += 1
            elif affiliation.subdivision == Subdivision.FCS:
                fcs_count += 1
        
        return AffiliationCountBySeasonResult(query.season_ID, fbs_count, fcs_count)
