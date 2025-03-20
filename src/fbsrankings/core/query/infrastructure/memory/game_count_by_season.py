from fbsrankings.messages.query import GameCountBySeasonQuery
from fbsrankings.messages.query import GameCountBySeasonResult
from fbsrankings.storage.memory import Storage


class GameCountBySeasonQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: GameCountBySeasonQuery) -> GameCountBySeasonResult:
        return GameCountBySeasonResult(
            query_id=query.query_id,
            season_id=query.season_id,
            count=len(self._storage.game.for_season(query.season_id)),
        )
