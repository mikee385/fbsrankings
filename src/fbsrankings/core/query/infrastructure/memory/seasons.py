from fbsrankings.core.query.query.seasons import SeasonResult
from fbsrankings.core.query.query.seasons import SeasonsQuery
from fbsrankings.core.query.query.seasons import SeasonsResult
from fbsrankings.storage.memory import Storage


class SeasonsQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: SeasonsQuery) -> SeasonsResult:
        return SeasonsResult(
            [SeasonResult(item.id_, item.year) for item in self._storage.season.all_()],
        )
