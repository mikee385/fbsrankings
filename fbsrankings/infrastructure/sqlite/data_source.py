from fbsrankings.infrastructure.sqlite.storage import Storage
from fbsrankings.infrastructure.sqlite.read import QueryHandler
from fbsrankings.infrastructure.sqlite.write import Transaction


class DataSource (object):
    def __init__(self, database):
        self._database = database
        self._storage = Storage(self._database)
        
    def query_handler(self, query_bus):
        return QueryHandler(self._database, query_bus)
        
    def transaction(self, event_bus):
        return Transaction(self._database, event_bus)
