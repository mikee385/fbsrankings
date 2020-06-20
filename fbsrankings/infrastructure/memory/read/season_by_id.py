from typing import Optional

from fbsrankings.common import Query, QueryHandler
from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.query import SeasonByIDQuery, SeasonByIDResult


class SeasonByIDQueryHandler (QueryHandler):
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def handle(self, query: Query) -> Optional[SeasonByIDResult]:
        if not isinstance(query, SeasonByIDQuery):
            raise TypeError('query must be of type SeasonByIDQuery')

        season = self._storage.season.get(query.ID)
        if season is not None:
            return SeasonByIDResult(season.ID, season.year)
        else:
            return None
