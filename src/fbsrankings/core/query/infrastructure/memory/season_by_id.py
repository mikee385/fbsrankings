from typing import Optional

from fbsrankings.messages.query import SeasonByIDQuery
from fbsrankings.messages.query import SeasonByIDResult
from fbsrankings.storage.memory import Storage


class SeasonByIDQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: SeasonByIDQuery) -> Optional[SeasonByIDResult]:
        season = self._storage.season.get(query.season_id)
        if season is not None:
            return SeasonByIDResult(str(season.id_), season.year)
        return None
