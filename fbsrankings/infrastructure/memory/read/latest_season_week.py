from typing import Dict
from typing import List
from typing import Optional

from fbsrankings.domain import GameStatus
from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.query import LatestSeasonWeekQuery
from fbsrankings.query import LatestSeasonWeekResult


class _Data(object):
    def __init__(self) -> None:
        self.has_completed = False
        self.has_scheduled = False


class LatestSeasonWeekQueryHandler(object):
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(
        self, query: LatestSeasonWeekQuery,
    ) -> Optional[LatestSeasonWeekResult]:
        for season in sorted(
            self._storage.season.all(), key=lambda s: s.year, reverse=True,
        ):
            season_data = _Data()
            weeks: Dict[int, _Data] = {}
            for game in self._storage.game.for_season(season.ID):
                week_data = weeks.setdefault(game.week, _Data())
                if game.status == GameStatus.COMPLETED.name:
                    season_data.has_completed = True
                    week_data.has_completed = True
                elif game.status == GameStatus.SCHEDULED.name:
                    season_data.has_scheduled = True
                    week_data.has_scheduled = True

            if season_data.has_scheduled is False and season_data.has_completed is True:
                return LatestSeasonWeekResult(season.ID, season.year, None)

            completed_weeks: List[int] = []
            for week, data in weeks.items():
                if data.has_scheduled is False and data.has_completed is True:
                    completed_weeks.append(week)
            if len(completed_weeks) > 0:
                sorted_weeks = sorted(completed_weeks, reverse=True)
                return LatestSeasonWeekResult(season.ID, season.year, sorted_weeks[0])

        return None
