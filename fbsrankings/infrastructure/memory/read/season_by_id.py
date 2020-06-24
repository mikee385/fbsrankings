from typing import Optional

from fbsrankings.common import QueryHandler
from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.query import SeasonByIDQuery, SeasonByIDResult


class SeasonByIDQueryHandler(QueryHandler[SeasonByIDQuery, Optional[SeasonByIDResult]]):
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def handle(self, query: SeasonByIDQuery) -> Optional[SeasonByIDResult]:
        season = self._storage.season.get(query.ID)
        if season is not None:
            return SeasonByIDResult(season.ID, season.year)
        else:
            return None
