from fbsrankings.messages.query import SeasonByYearQuery
from fbsrankings.messages.query import SeasonByYearResult
from fbsrankings.messages.query import SeasonByYearValue
from fbsrankings.storage.tinydb import Storage


class SeasonByYearQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: SeasonByYearQuery) -> SeasonByYearResult:
        item = self._storage.cache_season_by_year.get(query.year)

        return (
            SeasonByYearResult(
                season=SeasonByYearValue(season_id=item["id_"], year=item["year"]),
            )
            if item is not None
            else SeasonByYearResult(season=None)
        )
