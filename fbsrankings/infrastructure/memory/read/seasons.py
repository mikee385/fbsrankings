from fbsrankings.common import QueryHandler
from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.query import SeasonResult, SeasonsQuery, SeasonsResult


class SeasonsQueryHandler(QueryHandler[SeasonsQuery]):
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def handle(self, query: SeasonsQuery) -> SeasonsResult:
        return SeasonsResult(
            [SeasonResult(item.ID, item.year) for item in self._storage.season.all()]
        )
