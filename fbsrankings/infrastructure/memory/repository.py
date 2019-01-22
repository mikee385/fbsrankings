from fbsrankings.common import EventBus
from fbsrankings.domain import Repository as BaseRepository
from fbsrankings.infrastructure.memory import SeasonDataStore, SeasonRepository, TeamDataStore, TeamRepository, AffiliationDataStore, AffiliationRepository, GameDataStore, GameRepository


class DataStore (BaseRepository):
    def __init__(self, event_bus):
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self.event_bus = event_bus
        
        super().__init__(SeasonDataStore(event_bus), TeamDataStore(event_bus), AffiliationDataStore(event_bus), GameDataStore(event_bus))
        

class Repository (BaseRepository):
    def __init__(self, data_store, event_bus):
        if not isinstance(data_store, DataStore):
            raise TypeError('data_store must be of type DataStore')
        
        super().__init__(SeasonRepository(data_store.season, event_bus), TeamRepository(data_store.team, event_bus), AffiliationRepository(data_store.affiliation, event_bus), GameRepository(data_store.game, event_bus))
