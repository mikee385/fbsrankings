from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.infrastructure.memory.read import QueryHandler
from fbsrankings.infrastructure.memory.write import Transaction


class DataSource (object):
    def __init__(self):
        self._storage = Storage()
        
    def query_handler(self, query_bus):
        return QueryHandler(self._storage, query_bus)
        
    def transaction(self, event_bus):
        return Transaction(self._storage, event_bus)
