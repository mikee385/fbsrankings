from fbsrankings.common import EventBus
from fbsrankings.domain import Season, SeasonID, SeasonRepository as BaseRepository


class SeasonRepository(BaseRepository):
    def __init__(self, event_bus):
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._event_bus = event_bus
        
        self._season_id_dict = {}
        self._season_year_dict = {}
    
    def add(self, season):
        if not isinstance(season, Season):
            raise TypeError('season must be of type Season')
        
        if season.year in self._season_year_dict:
            raise ValueError(f'Season already exists for year {season.year}')

        self._season_id_dict[season.ID] = season
        self._season_year_dict[season.year] = season

    def find_by_ID(self, ID):
        if not isinstance(ID, SeasonID):
            raise TypeError('ID must be of type SeasonID')
        return self._season_id_dict.get(ID)
        
    def find_by_year(self, year):
        return self._season_year_dict.get(year)
        
    def all(self):
        return self._season_year_dict.values()
