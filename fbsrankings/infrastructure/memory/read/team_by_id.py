from typing import Optional

from fbsrankings.common import Query, QueryHandler
from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.query import TeamByIDQuery, TeamByIDResult


class TeamByIDQueryHandler (QueryHandler):
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def handle(self, query: Query) -> Optional[TeamByIDResult]:
        if not isinstance(query, TeamByIDQuery):
            raise TypeError('query must be of type TeamByIDQuery')

        team = self._storage.team.get(query.ID)
        if team is not None:
            return TeamByIDResult(team.ID, team.name)
        else:
            return None
