from typing import Optional

from fbsrankings.core.query.query.season_by_id import SeasonByIDQuery
from fbsrankings.core.query.query.season_by_id import SeasonByIDResult
from fbsrankings.storage.memory import Storage


class SeasonByIDQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: SeasonByIDQuery) -> Optional[SeasonByIDResult]:
        season = self._storage.season.get(query.id_)
        if season is not None:
            return SeasonByIDResult(season.id_, season.year)
        return None
