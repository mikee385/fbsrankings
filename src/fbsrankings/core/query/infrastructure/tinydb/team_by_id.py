from typing import Optional
from uuid import UUID

from fbsrankings.core.query.query.team_by_id import TeamByIDQuery
from fbsrankings.core.query.query.team_by_id import TeamByIDResult
from fbsrankings.storage.tinydb import Storage


class TeamByIDQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: TeamByIDQuery) -> Optional[TeamByIDResult]:
        item = self._storage.cache_team_by_id.get(str(query.id_))

        return (
            TeamByIDResult(UUID(item["id_"]), item["name"])
            if item is not None
            else None
        )
