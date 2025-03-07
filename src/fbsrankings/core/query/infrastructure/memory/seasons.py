from fbsrankings.messages.query import SeasonResult
from fbsrankings.messages.query import SeasonsQuery
from fbsrankings.messages.query import SeasonsResult
from fbsrankings.storage.memory import Storage


class SeasonsQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: SeasonsQuery) -> SeasonsResult:
        return SeasonsResult(
            [
                SeasonResult(str(item.id_), item.year)
                for item in self._storage.season.all_()
            ],
        )
