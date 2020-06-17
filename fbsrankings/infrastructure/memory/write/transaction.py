from fbsrankings.common import EventBus, EventRecorder
from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.infrastructure.memory.write import SeasonRepository, TeamRepository, AffiliationRepository, GameRepository


class Transaction (object):
    def __init__(self, storage, bus):
        if not isinstance(storage, Storage):
            raise TypeError('storage must be of type Storage')
        
        if not isinstance(bus, EventBus):
            raise TypeError('bus must be of type EventBus')
        self._bus = EventRecorder(bus)
        
        self.season = SeasonRepository(storage.season, self._bus)
        self.team = TeamRepository(storage.team, self._bus)
        self.affiliation = AffiliationRepository(storage.affiliation, self._bus)
        self.game = GameRepository(storage.game, self._bus)

    def commit(self):
        for event in self._bus.events:
            handled = False
        
            handled = self.season.handle(event) or handled
            handled = self.team.handle(event) or handled
            handled = self.affiliation.handle(event) or handled
            handled = self.game.handle(event) or handled
            
            if not handled:
                raise ValueError(f'Unknown event type: {type(event)}')
                
        self._bus.clear()
        
    def rollback(self):
        self._bus.clear()
        
    def close(self):
        self._bus.clear()
    
    def __enter__(self):
        return self
        
    def __exit__(self, type, value, traceback):
        self.close()
        return False
