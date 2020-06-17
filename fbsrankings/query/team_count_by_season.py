from fbsrankings.common import Query


class TeamCountBySeasonQuery (Query):
    def __init__(self, season_ID):
        self.season_ID = season_ID
    
    
class TeamCountBySeasonResult (object):
    def __init__(self, season_ID, count):
        self.season_ID = season_ID
        self.count = count
