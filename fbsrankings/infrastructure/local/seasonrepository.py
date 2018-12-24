from uuid import uuid4

from fbsrankings.domain.season import Season, SeasonID, SeasonRepository as BaseRepository


class SeasonRepository(BaseRepository):
    def __init__(self):
        self._season_id_dict = {}
        self._season_year_dict = {}
    
    def AddSeason(self, year, *args, **kwargs):
        if year in self._season_year_dict:
            raise ValueError('Season already exists for year ' + str(year))
            
        ID = SeasonID(uuid4())
        value = Season(ID, year, *args, **kwargs)
        
        self._season_id_dict[ID] = value
        self._season_year_dict[year] = value
        
        return value

    def FindSeason(self, ID):
        if not isinstance(ID, SeasonID):
            raise TypeError('ID must be of type SeasonID')
        return self._season_id_dict.get(ID)
        
    def FindSeasonByYear(self, year):
        return self._season_year_dict.get(year)
        
    def AllSeasons(self):
        return self._season_year_dict.values()
