from typing import Optional
from uuid import UUID

from fbsrankings.core.query.query.season_by_id import SeasonByIDQuery
from fbsrankings.core.query.query.season_by_id import SeasonByIDResult
from fbsrankings.storage.tinydb import Storage


class SeasonByIDQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: SeasonByIDQuery) -> Optional[SeasonByIDResult]:
        item = self._storage.cache_season_by_id.get(str(query.id_))

        return (
            SeasonByIDResult(UUID(item["id_"]), item["year"])
            if item is not None
            else None
        )
