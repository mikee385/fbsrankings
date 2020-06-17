from fbsrankings.common import Query


class TeamByIDQuery (Query):
    def __init__(self, ID):
        self.ID = ID
    
    
class TeamByIDResult (object):
    def __init__(self, ID, name):
        self.ID = ID
        self.name = name
