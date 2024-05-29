from fbsrankings.shared.query import GameCountBySeasonQuery
from fbsrankings.shared.query import GameCountBySeasonResult
from fbsrankings.storage.memory import Storage


class GameCountBySeasonQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: GameCountBySeasonQuery) -> GameCountBySeasonResult:
        return GameCountBySeasonResult(
            query.season_id,
            len(self._storage.game.for_season(query.season_id)),
        )
