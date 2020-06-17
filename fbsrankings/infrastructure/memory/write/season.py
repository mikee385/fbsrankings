from fbsrankings.domain import Season, SeasonRepository as BaseRepository
from fbsrankings.event import SeasonRegisteredEvent
from fbsrankings.infrastructure.memory.storage import SeasonStorage, SeasonDto
        

class SeasonRepository (BaseRepository):
    def __init__(self, storage, bus):
        super().__init__(bus)
        
        if not isinstance(storage, SeasonStorage):
            raise TypeError('storage must be of type SeasonStorage')
        self._storage = storage
        
    def _to_season(self, dto):
        if dto is not None:
            return Season(self._bus, dto.ID, dto.year)
        return None

    def find_by_ID(self, ID):
        return self._to_season(self._storage.find_by_ID(ID))
        
    def find_by_year(self, year):
        return self._to_season(self._storage.find_by_year(year))
        
    def all(self):
        return [self._to_season(item) for item in self._storage.all()]
        
    def handle(self, event):
        if isinstance(event, SeasonRegisteredEvent):
            self._handle_season_registered(event)
            return True
        else:
            return False
        
    def _handle_season_registered(self, event):
        self._storage.add(SeasonDto(event.ID, event.year))
