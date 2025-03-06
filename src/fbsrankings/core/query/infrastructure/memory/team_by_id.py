from typing import Optional

from fbsrankings.messages.query import TeamByIDQuery
from fbsrankings.messages.query import TeamByIDResult
from fbsrankings.storage.memory import Storage


class TeamByIDQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: TeamByIDQuery) -> Optional[TeamByIDResult]:
        team = self._storage.team.get(query.team_id)
        if team is not None:
            return TeamByIDResult(team.id_, team.name)
        return None
