from fbsrankings.messages.query import SeasonResult
from fbsrankings.messages.query import SeasonsQuery
from fbsrankings.messages.query import SeasonsResult
from fbsrankings.storage.memory import Storage


class SeasonsQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: SeasonsQuery) -> SeasonsResult:
        return SeasonsResult(
            query_id=query.query_id,
            seasons=[
                SeasonResult(season_id=str(item.id_), year=item.year)
                for item in self._storage.season.all_()
            ],
        )
