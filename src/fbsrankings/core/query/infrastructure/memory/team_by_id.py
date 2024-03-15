from typing import Optional

from fbsrankings.core.query.query.team_by_id import TeamByIDQuery
from fbsrankings.core.query.query.team_by_id import TeamByIDResult
from fbsrankings.storage.memory import Storage


class TeamByIDQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: TeamByIDQuery) -> Optional[TeamByIDResult]:
        team = self._storage.team.get(query.id_)
        if team is not None:
            return TeamByIDResult(team.id_, team.name)
        return None
