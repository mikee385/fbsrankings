from fbsrankings.common import EventBus
from fbsrankings.domain import Season, SeasonRepository
from fbsrankings.event import SeasonRegisteredEvent


class SeasonDto (object):
    def __init__(self, ID, year):
        self.ID = ID
        self.year = year


class SeasonDataSource (object):
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
        

class SeasonQueryHandler (SeasonRepository):
    def __init__(self, data_source, event_bus):
        super().__init__(event_bus)
        
        if not isinstance(data_source, SeasonDataSource):
            raise TypeError('repository must be of type SeasonDataSource')
        self._data_source = data_source
        
    def _to_season(self, dto):
        if dto is not None:
            return Season(self._event_bus, dto.ID, dto.year)
        return None

    def find_by_ID(self, ID):
        return self._to_season(self._data_source.find_by_ID(ID))
        
    def find_by_year(self, year):
        return self._to_season(self._data_source.find_by_year(year))
        
    def all(self):
        return [self._to_season(item) for item in self._data_source.all()]
        

class SeasonEventHandler (object):
    def __init__(self, data_source, event_bus):
        if not isinstance(data_source, SeasonDataSource):
            raise TypeError('data_source must be of type SeasonDataSource')
        self._data_source = data_source
        
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._event_bus = event_bus
        
    def handle(self, event):
        if isinstance(event, SeasonRegisteredEvent):
            self._handle_season_registered(event)
            return True
        else:
            return False
        
    def _handle_season_registered(self, event):
        self._data_source.add(SeasonDto(event.ID, event.year))
