from fbsrankings.common import EventBus, EventRecorder
from fbsrankings.infrastructure import Transaction as BaseTransaction
from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.infrastructure.memory.write import SeasonRepository, TeamRepository, AffiliationRepository, GameRepository


class Transaction (BaseTransaction):
    def __init__(self, storage: Storage, bus: EventBus) -> None:
        self._bus = EventRecorder(bus)

        self._season = SeasonRepository(storage.season, self._bus)
        self._team = TeamRepository(storage.team, self._bus)
        self._affiliation = AffiliationRepository(storage.affiliation, self._bus)
        self._game = GameRepository(storage.game, self._bus)
        
    @property
    def season(self) -> SeasonRepository:
        return self._season
        
    @property
    def team(self) -> TeamRepository:
        return self._team
        
    @property
    def affiliation(self) -> AffiliationRepository:
        return self._affiliation
        
    @property
    def game(self) -> GameRepository:
        return self._game

    def commit(self) -> None:
        for event in self._bus.events:
            handled = False
        
            handled = self._season.handle(event) or handled
            handled = self._team.handle(event) or handled
            handled = self._affiliation.handle(event) or handled
            handled = self._game.handle(event) or handled
            
            if not handled:
                raise ValueError(f'Unknown event type: {type(event)}')
                
        self._bus.clear()
        
    def rollback(self) -> None:
        self._bus.clear()
        
    def close(self) -> None:
        self._bus.clear()
