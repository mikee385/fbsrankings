from typing import Optional

from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.query import TeamByIDQuery
from fbsrankings.query import TeamByIDResult


class TeamByIDQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: TeamByIDQuery) -> Optional[TeamByIDResult]:
        team = self._storage.team.get(query.id_)
        if team is not None:
            return TeamByIDResult(team.id_, team.name)
        return None
