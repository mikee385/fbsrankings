from typing import Optional

from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.query import SeasonByYearQuery
from fbsrankings.query import SeasonByYearResult


class SeasonByYearQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: SeasonByYearQuery) -> Optional[SeasonByYearResult]:
        season = self._storage.season.find(query.year)
        if season is not None:
            return SeasonByYearResult(season.id, season.year)
        else:
            return None
