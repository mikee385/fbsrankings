from fbsrankings.common import Query


class SeasonsQuery (Query):
    pass
    
    
class SeasonsResult (object):
    def __init__(self, seasons):
        self.seasons = seasons
    

class SeasonResult (object):
    def __init__(self, ID, year):
        self.ID = ID
        self.year = year
