from fbsrankings.domain import Team, TeamRepository as BaseRepository
from fbsrankings.event import TeamRegisteredEvent
from fbsrankings.infrastructure.memory.storage import TeamStorage, TeamDto
        

class TeamRepository (BaseRepository):
    def __init__(self, storage, bus):
        super().__init__(bus)
        
        if not isinstance(storage, TeamStorage):
            raise TypeError('storage must be of type TeamStorage')
        self._storage = storage
        
    def _to_team(self, dto):
        if dto is not None:
            return Team(self._bus, dto.ID, dto.name)
        return None

    def find_by_ID(self, ID):
        return self._to_team(self._storage.find_by_ID(ID))
        
    def find_by_name(self, name):
        return self._to_team(self._storage.find_by_name(name))
        
    def all(self):
        return [self._to_team(item) for item in self._storage.all()]
        
    def handle(self, event):
        if isinstance(event, TeamRegisteredEvent):
            self._handle_team_registered(event)
            return True
        else:
            return False
        
    def _handle_team_registered(self, event):
        self._storage.add(TeamDto(event.ID, event.name))
