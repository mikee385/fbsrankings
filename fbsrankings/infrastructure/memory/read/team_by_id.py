from fbsrankings.query import TeamByIDResult
from fbsrankings.infrastructure.memory.storage import Storage


class TeamByIDQueryHandler (object):
    def __init__(self, storage):
        if not isinstance(storage, Storage):
            raise TypeError('storage must be of type Storage')
        self._storage = storage

    def handle(self, query):
        team = self._storage.team.get(query.ID)
        if team is not None:
            return TeamByIDResult(team.ID, team.name)
        else:
            return None
