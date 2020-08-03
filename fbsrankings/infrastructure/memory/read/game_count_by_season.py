from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.query import GameCountBySeasonQuery
from fbsrankings.query import GameCountBySeasonResult


class GameCountBySeasonQueryHandler(object):
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: GameCountBySeasonQuery) -> GameCountBySeasonResult:
        return GameCountBySeasonResult(
            query.season_ID, len(self._storage.game.for_season(query.season_ID)),
        )
