from fbsrankings.query import SeasonByIDResult
from fbsrankings.infrastructure.memory.storage import Storage


class SeasonByIDQueryHandler (object):
    def __init__(self, storage):
        if not isinstance(storage, Storage):
            raise TypeError('storage must be of type Storage')
        self._storage = storage

    def handle(self, query):
        season = self._storage.season.get(query.ID)
        if season is not None:
            return SeasonByIDResult(season.ID, season.year)
        else:
            return None
