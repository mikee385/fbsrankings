from fbsrankings.query import SeasonsResult, SeasonResult
from fbsrankings.infrastructure.memory.storage import Storage


class SeasonsQueryHandler (object):
    def __init__(self, storage):
        if not isinstance(storage, Storage):
            raise TypeError('storage must be of type Storage')
        self._storage = storage

    def handle(self, query):
        return SeasonsResult([SeasonResult(item.ID, item.year) for item in self._storage.season.all()])
