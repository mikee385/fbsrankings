class SeasonDto (object):
    def __init__(self, ID, year):
        self.ID = ID
        self.year = year


class SeasonStorage (object):
    def __init__(self):
        self._season_id_dict = {}
        self._season_year_dict = {}
    
    def add(self, season):
        if not isinstance(season, SeasonDto):
            raise TypeError('season must be of type SeasonDto')
        
        if season.year in self._season_year_dict:
            raise ValueError(f'Season already exists for year {season.year}')

        self._season_id_dict[season.ID] = season
        self._season_year_dict[season.year] = season

    def find_by_ID(self, ID):
        return self._season_id_dict.get(ID)
        
    def find_by_year(self, year):
        return self._season_year_dict.get(year)
        
    def all(self):
        return [item for item in self._season_year_dict.values()]
