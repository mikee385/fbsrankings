from typing import Optional

from fbsrankings.core.query.query.season_by_year import SeasonByYearQuery
from fbsrankings.core.query.query.season_by_year import SeasonByYearResult
from fbsrankings.storage.memory import Storage


class SeasonByYearQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: SeasonByYearQuery) -> Optional[SeasonByYearResult]:
        season = self._storage.season.find(query.year)
        if season is not None:
            return SeasonByYearResult(season.id_, season.year)
        return None
