from typing import Optional

from fbsrankings.messages.query import SeasonByIDQuery
from fbsrankings.messages.query import SeasonByIDResult
from fbsrankings.storage.tinydb import Storage


class SeasonByIDQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: SeasonByIDQuery) -> Optional[SeasonByIDResult]:
        item = self._storage.cache_season_by_id.get(query.season_id)

        return SeasonByIDResult(item["id_"], item["year"]) if item is not None else None
