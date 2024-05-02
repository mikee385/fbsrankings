from typing import Optional
from uuid import UUID

from fbsrankings.core.query.query.season_by_year import SeasonByYearQuery
from fbsrankings.core.query.query.season_by_year import SeasonByYearResult
from fbsrankings.storage.tinydb import Storage


class SeasonByYearQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: SeasonByYearQuery) -> Optional[SeasonByYearResult]:
        item = self._storage.cache_season_by_year.get(query.year)

        return (
            SeasonByYearResult(UUID(item["id_"]), item["year"])
            if item is not None
            else None
        )
