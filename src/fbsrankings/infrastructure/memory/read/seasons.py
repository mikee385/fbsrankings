from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.query import SeasonResult
from fbsrankings.query import SeasonsQuery
from fbsrankings.query import SeasonsResult


class SeasonsQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: SeasonsQuery) -> SeasonsResult:
        return SeasonsResult(
            [SeasonResult(item.id_, item.year) for item in self._storage.season.all_()],
        )
