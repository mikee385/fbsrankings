from uuid import uuid4

from fbsrankings.domain.season import Season, SeasonID, SeasonRepository as BaseRepository


class SeasonRepository(BaseRepository):
    def __init__(self):
        self._season_id_dict = {}
        self._season_year_dict = {}
    
    def add_season(self, year, *args, **kwargs):
        if year in self._season_year_dict:
            raise ValueError('Season already exists for year ' + str(year))
            
        ID = SeasonID(uuid4())
        value = Season(ID, year, *args, **kwargs)
        
        self._season_id_dict[ID] = value
        self._season_year_dict[year] = value
        
        return value

    def find_season(self, ID):
        if not isinstance(ID, SeasonID):
            raise TypeError('ID must be of type SeasonID')
        return self._season_id_dict.get(ID)
        
    def find_season_by_year(self, year):
        return self._season_year_dict.get(year)
        
    def all_seasons(self):
        return self._season_year_dict.values()
