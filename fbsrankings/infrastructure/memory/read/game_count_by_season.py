from fbsrankings.common import Query, QueryHandler
from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.query import GameCountBySeasonQuery, GameCountBySeasonResult


class GameCountBySeasonQueryHandler(QueryHandler):
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def handle(self, query: Query) -> GameCountBySeasonResult:
        if not isinstance(query, GameCountBySeasonQuery):
            raise TypeError("query must be of type GameCountBySeasonQuery")

        return GameCountBySeasonResult(
            query.season_ID, len(self._storage.game.by_season(query.season_ID))
        )
