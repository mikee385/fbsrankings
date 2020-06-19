from fbsrankings.domain import Season, SeasonRepository as BaseRepository
from fbsrankings.event import SeasonCreatedEvent
from fbsrankings.infrastructure.memory.storage import SeasonStorage, SeasonDto
        

class SeasonRepository (BaseRepository):
    def __init__(self, storage, bus):
        super().__init__(bus)
        
        if not isinstance(storage, SeasonStorage):
            raise TypeError('storage must be of type SeasonStorage')
        self._storage = storage

    def get(self, ID):
        return self._to_season(self._storage.get(ID))
        
    def find(self, year):
        return self._to_season(self._storage.find(year))
        
    def _to_season(self, dto):
        if dto is not None:
            return Season(self._bus, dto.ID, dto.year)
        return None
        
    def handle(self, event):
        if isinstance(event, SeasonCreatedEvent):
            self._handle_season_created(event)
            return True
        else:
            return False
        
    def _handle_season_created(self, event):
        self._storage.add(SeasonDto(event.ID, event.year))
