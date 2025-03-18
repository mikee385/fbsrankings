from fbsrankings.messages.query import SeasonByIDQuery
from fbsrankings.messages.query import SeasonByIDResult
from fbsrankings.messages.query import SeasonByIDValue
from fbsrankings.storage.tinydb import Storage


class SeasonByIDQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: SeasonByIDQuery) -> SeasonByIDResult:
        item = self._storage.cache_season_by_id.get(query.season_id)

        if item is not None:
            return SeasonByIDResult(
                season=SeasonByIDValue(season_id=item["id_"], year=item["year"]),
            )

        return SeasonByIDResult(season=None)
