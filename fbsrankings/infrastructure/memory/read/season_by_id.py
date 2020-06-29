from typing import Optional

from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.query import SeasonByIDQuery
from fbsrankings.query import SeasonByIDResult


class SeasonByIDQueryHandler(object):
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: SeasonByIDQuery) -> Optional[SeasonByIDResult]:
        season = self._storage.season.get(query.ID)
        if season is not None:
            return SeasonByIDResult(season.ID, season.year)
        else:
            return None
