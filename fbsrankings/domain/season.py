from enum import Enum
from fbsrankings.common.identifier import Identifier


class SeasonSection(Enum):
    PRESEASON = 0
    REGULAR_SEASON = 1
    POSTSEASON = 2


class SeasonID (Identifier):
    pass


class Season (object):
    def __init__(self, ID, year):
        if not isinstance(ID, SeasonID):
            raise TypeError('ID must be of type SeasonID')
        self.ID = ID
        self.year = year


class SeasonRepository (object):
    def AddSeason(self, year, *args, **kwargs):
        pass

    def FindSeason(self, ID):
        pass
        
    def FindSeasonByYear(self, year):
        pass
        
    def AllSeasons(self):
        pass
        