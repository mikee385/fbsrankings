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
    def add_season(self, year, *args, **kwargs):
        raise NotImplementedError

    def find_season(self, ID):
        raise NotImplementedError
        
    def find_season_by_year(self, year):
        raise NotImplementedError
        
    def all_seasons(self):
        raise NotImplementedError
        
