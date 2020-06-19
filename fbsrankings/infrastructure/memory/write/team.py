from fbsrankings.domain import Team, TeamRepository as BaseRepository
from fbsrankings.event import TeamCreatedEvent
from fbsrankings.infrastructure.memory.storage import TeamStorage, TeamDto
        

class TeamRepository (BaseRepository):
    def __init__(self, storage, bus):
        super().__init__(bus)
        
        if not isinstance(storage, TeamStorage):
            raise TypeError('storage must be of type TeamStorage')
        self._storage = storage

    def get(self, ID):
        return self._to_team(self._storage.get(ID))
        
    def find(self, name):
        return self._to_team(self._storage.find(name))
        
    def _to_team(self, dto):
        if dto is not None:
            return Team(self._bus, dto.ID, dto.name)
        return None
        
    def handle(self, event):
        if isinstance(event, TeamCreatedEvent):
            self._handle_team_created(event)
            return True
        else:
            return False
        
    def _handle_team_created(self, event):
        self._storage.add(TeamDto(event.ID, event.name))
