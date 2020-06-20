from uuid import UUID

from fbsrankings.common import Query


class SeasonByIDQuery (Query):
    def __init__(self, ID: UUID) -> None:
        self.ID = ID
    
    
class SeasonByIDResult (object):
    def __init__(self, ID: UUID, year: int) -> None:
        self.ID = ID
        self.year = year
