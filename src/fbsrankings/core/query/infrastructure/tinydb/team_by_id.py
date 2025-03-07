from typing import Optional

from fbsrankings.messages.query import TeamByIDQuery
from fbsrankings.messages.query import TeamByIDResult
from fbsrankings.storage.tinydb import Storage


class TeamByIDQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: TeamByIDQuery) -> Optional[TeamByIDResult]:
        item = self._storage.cache_team_by_id.get(query.team_id)

        return TeamByIDResult(item["id_"], item["name"]) if item is not None else None
