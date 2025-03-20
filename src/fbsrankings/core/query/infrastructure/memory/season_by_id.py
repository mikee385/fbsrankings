from fbsrankings.messages.query import SeasonByIDQuery
from fbsrankings.messages.query import SeasonByIDResult
from fbsrankings.messages.query import SeasonByIDValue
from fbsrankings.storage.memory import Storage


class SeasonByIDQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: SeasonByIDQuery) -> SeasonByIDResult:
        season = self._storage.season.get(query.season_id)
        if season is not None:
            return SeasonByIDResult(
                query_id=query.query_id,
                season=SeasonByIDValue(season_id=str(season.id_), year=season.year),
            )
        return SeasonByIDResult(query_id=query.query_id, season=None)
