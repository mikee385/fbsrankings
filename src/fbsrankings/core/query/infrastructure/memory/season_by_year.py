from fbsrankings.messages.query import SeasonByYearQuery
from fbsrankings.messages.query import SeasonByYearResult
from fbsrankings.messages.query import SeasonByYearValue
from fbsrankings.storage.memory import Storage


class SeasonByYearQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: SeasonByYearQuery) -> SeasonByYearResult:
        season = self._storage.season.find(query.year)
        if season is not None:
            return SeasonByYearResult(
                season=SeasonByYearValue(season_id=str(season.id_), year=season.year),
            )
        return SeasonByYearResult(season=None)
