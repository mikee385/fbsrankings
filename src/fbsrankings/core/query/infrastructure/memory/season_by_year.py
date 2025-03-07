from typing import Optional

from fbsrankings.messages.query import SeasonByYearQuery
from fbsrankings.messages.query import SeasonByYearResult
from fbsrankings.storage.memory import Storage


class SeasonByYearQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: SeasonByYearQuery) -> Optional[SeasonByYearResult]:
        season = self._storage.season.find(query.year)
        if season is not None:
            return SeasonByYearResult(str(season.id_), season.year)
        return None
