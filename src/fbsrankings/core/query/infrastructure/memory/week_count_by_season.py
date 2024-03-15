from fbsrankings.core.query.query.week_count_by_season import WeekCountBySeasonQuery
from fbsrankings.core.query.query.week_count_by_season import WeekCountBySeasonResult
from fbsrankings.storage.memory import Storage


class WeekCountBySeasonQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: WeekCountBySeasonQuery) -> WeekCountBySeasonResult:
        return WeekCountBySeasonResult(
            query.season_id,
            max(g.week for g in self._storage.game.for_season(query.season_id)),
        )
