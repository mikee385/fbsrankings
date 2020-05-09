from fbsrankings.common import EventBus
from fbsrankings.domain import Season, SeasonRepository as BaseRepository
from fbsrankings.event import SeasonRegisteredEvent


class SeasonDto (object):
    def __init__(self, ID, year):
        self.ID = ID
        self.year = year


class SeasonDataStore (object):
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
        

class SeasonRepository (BaseRepository):
    def __init__(self, data_store, event_bus):
        if not isinstance(data_store, SeasonDataStore):
            raise TypeError('repository must be of type SeasonDataStore')
        self._data_store = data_store
        
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._event_bus = event_bus
        
    def _to_season(self, dto):
        if dto is not None:
            return Season(self._event_bus, dto.ID, dto.year)
        return None

    def find_by_ID(self, ID):
        return self._to_season(self._data_store.find_by_ID(ID))
        
    def find_by_year(self, year):
        return self._to_season(self._data_store.find_by_year(year))
        
    def all(self):
        return [self._to_season(item) for item in self._data_store.all()]
        
    def try_handle_event(self, event):
        if isinstance(event, SeasonRegisteredEvent):
            self._data_store.add(SeasonDto(event.ID, event.year))
            return True
        else:
            return False
