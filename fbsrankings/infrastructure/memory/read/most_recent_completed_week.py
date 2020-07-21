from typing import Dict
from typing import List
from typing import Optional

from fbsrankings.domain import GameStatus
from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.query import MostRecentCompletedWeekQuery
from fbsrankings.query import MostRecentCompletedWeekResult


class _WeekData(object):
    def __init__(self) -> None:
        self.has_completed = False
        self.has_scheduled = False


class MostRecentCompletedWeekQueryHandler(object):
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(
        self, query: MostRecentCompletedWeekQuery
    ) -> Optional[MostRecentCompletedWeekResult]:
        for season in sorted(
            self._storage.season.all(), key=lambda s: s.year, reverse=True
        ):
            weeks: Dict[int, _WeekData] = {}
            for game in self._storage.game.for_season(season.ID):
                week_data = weeks.setdefault(game.week, _WeekData())
                if game.status == GameStatus.COMPLETED.name:
                    week_data.has_completed = True
                elif game.status == GameStatus.SCHEDULED.name:
                    week_data.has_scheduled = True

            completed_weeks: List[int] = []
            for week, data in weeks.items():
                if data.has_scheduled is False and data.has_completed is True:
                    completed_weeks.append(week)
            if len(completed_weeks) > 0:
                sorted_weeks = sorted(completed_weeks, reverse=True)
                return MostRecentCompletedWeekResult(
                    season.ID, season.year, sorted_weeks[0]
                )

        return None
