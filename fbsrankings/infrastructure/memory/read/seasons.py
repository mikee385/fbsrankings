from fbsrankings.common import Query, QueryHandler
from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.query import SeasonResult, SeasonsQuery, SeasonsResult


class SeasonsQueryHandler(QueryHandler):
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def handle(self, query: Query) -> SeasonsResult:
        if not isinstance(query, SeasonsQuery):
            raise TypeError("query must be of type SeasonsQuery")

        return SeasonsResult(
            [SeasonResult(item.ID, item.year) for item in self._storage.season.all()]
        )
