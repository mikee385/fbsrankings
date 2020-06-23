from typing import Optional

from fbsrankings.common import QueryHandler
from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.query import TeamByIDQuery, TeamByIDResult


class TeamByIDQueryHandler(QueryHandler[TeamByIDQuery]):
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def handle(self, query: TeamByIDQuery) -> Optional[TeamByIDResult]:
        team = self._storage.team.get(query.ID)
        if team is not None:
            return TeamByIDResult(team.ID, team.name)
        else:
            return None
