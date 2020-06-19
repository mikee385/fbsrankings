class SeasonDto (object):
    def __init__(self, ID, year):
        self.ID = ID
        self.year = year


class SeasonStorage (object):
    def __init__(self):
        self._by_ID = {}
        self._by_key = {}
    
    def add(self, season):
        if not isinstance(season, SeasonDto):
            raise TypeError('season must be of type SeasonDto')
        
        if season.year in self._by_key:
            raise ValueError(f'Season already exists for year {season.year}')

        self._by_ID[season.ID] = season
        self._by_key[season.year] = season

    def get(self, ID):
        return self._by_ID.get(ID)
        
    def find(self, year):
        return self._by_key.get(year)
        
    def all(self):
        return self._by_key.values()
