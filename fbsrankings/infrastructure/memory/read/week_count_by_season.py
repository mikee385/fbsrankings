from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.query import WeekCountBySeasonQuery
from fbsrankings.query import WeekCountBySeasonResult


class WeekCountBySeasonQueryHandler(object):
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: WeekCountBySeasonQuery) -> WeekCountBySeasonResult:
        return WeekCountBySeasonResult(
            query.season_ID,
            max(g.week for g in self._storage.game.for_season(query.season_ID)),
        )
