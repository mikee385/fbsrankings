from fbsrankings.common import EventBus, QueryBus
from fbsrankings.infrastructure import QueryManagerFactory, TransactionFactory
from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.infrastructure.memory.read import QueryManager
from fbsrankings.infrastructure.memory.write import Transaction


class DataSource (QueryManagerFactory, TransactionFactory):
    def __init__(self) -> None:
        self._storage = Storage()
        
    def query_manager(self, query_bus: QueryBus) -> QueryManager:
        return QueryManager(self._storage, query_bus)
        
    def transaction(self, event_bus: EventBus) -> Transaction:
        return Transaction(self._storage, event_bus)
