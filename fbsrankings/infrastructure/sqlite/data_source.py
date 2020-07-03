import os

from fbsrankings.common import EventBus
from fbsrankings.common import QueryBus
from fbsrankings.infrastructure import QueryManagerFactory
from fbsrankings.infrastructure import TransactionFactory
from fbsrankings.infrastructure.sqlite.read import QueryManager
from fbsrankings.infrastructure.sqlite.storage import Storage
from fbsrankings.infrastructure.sqlite.write import Transaction


class DataSource(QueryManagerFactory, TransactionFactory):
    def __init__(self, database: str) -> None:
        if database == ":memory:":
            self._database = database
        elif os.path.isabs(database):
            self._database = database
        else:
            sqlite_dir = os.path.dirname(__file__)
            infrastructure_dir = os.path.dirname(sqlite_dir)
            package_dir = os.path.dirname(infrastructure_dir)
            self._database = os.path.join(os.path.abspath(package_dir), database)
        
        self._storage = Storage(self._database)

    def query_manager(self, query_bus: QueryBus) -> QueryManager:
        return QueryManager(self._database, query_bus)

    def transaction(self, event_bus: EventBus) -> Transaction:
        return Transaction(self._database, event_bus)
