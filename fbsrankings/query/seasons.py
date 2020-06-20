from typing import List
from uuid import UUID

from fbsrankings.common import Query


class SeasonsQuery (Query):
    pass
    

class SeasonResult (object):
    def __init__(self, ID: UUID, year: int) -> None:
        self.ID = ID
        self.year = year
    
    
class SeasonsResult (object):
    def __init__(self, seasons: List[SeasonResult]) -> None:
        self.seasons = seasons
