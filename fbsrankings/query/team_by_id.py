from uuid import UUID

from fbsrankings.common import Query


class TeamByIDQuery (Query):
    def __init__(self, ID: UUID) -> None:
        self.ID = ID
    
    
class TeamByIDResult (object):
    def __init__(self, ID: UUID, name: str) -> None:
        self.ID = ID
        self.name = name
