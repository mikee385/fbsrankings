from fbsrankings.query import TeamCountBySeasonResult
from fbsrankings.infrastructure.memory.storage import Storage


class TeamCountBySeasonQueryHandler (object):
    def __init__(self, storage):
        if not isinstance(storage, Storage):
            raise TypeError('storage must be of type Storage')
        self._storage = storage

    def handle(self, query):
        return TeamCountBySeasonResult(query.season_ID, len(self._storage.affiliation.by_season(query.season_ID)))
