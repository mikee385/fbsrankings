from fbsrankings.common import Query


class GameCountBySeasonQuery (Query):
    def __init__(self, season_ID):
        self.season_ID = season_ID
    
    
class GameCountBySeasonResult (object):
    def __init__(self, season_ID, count):
        self.season_ID = season_ID
        self.count = count
