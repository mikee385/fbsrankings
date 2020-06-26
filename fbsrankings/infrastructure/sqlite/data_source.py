from fbsrankings.common import EventBus
from fbsrankings.common import QueryBus
from fbsrankings.infrastructure import QueryManagerFactory
from fbsrankings.infrastructure import TransactionFactory
from fbsrankings.infrastructure.sqlite.read import QueryManager
from fbsrankings.infrastructure.sqlite.storage import Storage
from fbsrankings.infrastructure.sqlite.write import Transaction


class DataSource(QueryManagerFactory, TransactionFactory):
    def __init__(self, database: str) -> None:
        self._database = database
        self._storage = Storage(self._database)

    def query_manager(self, query_bus: QueryBus) -> QueryManager:
        return QueryManager(self._database, query_bus)

    def transaction(self, event_bus: EventBus) -> Transaction:
        return Transaction(self._database, event_bus)
