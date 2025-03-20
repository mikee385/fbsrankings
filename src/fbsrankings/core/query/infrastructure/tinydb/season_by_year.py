from fbsrankings.messages.query import SeasonByYearQuery
from fbsrankings.messages.query import SeasonByYearResult
from fbsrankings.messages.query import SeasonByYearValue
from fbsrankings.storage.tinydb import Storage


class SeasonByYearQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: SeasonByYearQuery) -> SeasonByYearResult:
        item = self._storage.cache_season_by_year.get(query.year)

        if item is not None:
            return SeasonByYearResult(
                query_id=query.query_id,
                season=SeasonByYearValue(season_id=item["id_"], year=item["year"]),
            )

        return SeasonByYearResult(query_id=query.query_id, season=None)
