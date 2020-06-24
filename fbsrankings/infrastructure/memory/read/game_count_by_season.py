from fbsrankings.common import QueryHandler
from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.query import GameCountBySeasonQuery, GameCountBySeasonResult


class GameCountBySeasonQueryHandler(
    QueryHandler[GameCountBySeasonQuery, GameCountBySeasonResult]
):
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def handle(self, query: GameCountBySeasonQuery) -> GameCountBySeasonResult:
        return GameCountBySeasonResult(
            query.season_ID, len(self._storage.game.by_season(query.season_ID))
        )
