from fbsrankings.common import Query


class AffiliationCountBySeasonQuery (Query):
    def __init__(self, season_ID):
        self.season_ID = season_ID
    
    
class AffiliationCountBySeasonResult (object):
    def __init__(self, season_ID, fbs_count, fcs_count):
        self.season_ID = season_ID
        self.fbs_count = fbs_count
        self.fcs_count = fcs_count
