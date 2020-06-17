from fbsrankings.query import GameCountBySeasonResult
from fbsrankings.infrastructure.memory.storage import Storage


class GameCountBySeasonQueryHandler (object):
    def __init__(self, storage):
        if not isinstance(storage, Storage):
            raise TypeError('storage must be of type Storage')
        self._storage = storage

    def handle(self, query):
        return GameCountBySeasonResult(query.season_ID, len(self._storage.game.find_by_season(query.season_ID)))
