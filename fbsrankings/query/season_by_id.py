from fbsrankings.common import Query


class SeasonByIDQuery (Query):
    def __init__(self, ID):
        self.ID = ID
    
    
class SeasonByIDResult (object):
    def __init__(self, ID, year):
        self.ID = ID
        self.year = year
