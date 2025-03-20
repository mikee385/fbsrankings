from fbsrankings.messages.enums import GameStatus
from fbsrankings.messages.query import LatestSeasonWeekQuery
from fbsrankings.messages.query import LatestSeasonWeekResult
from fbsrankings.messages.query import LatestSeasonWeekValue
from fbsrankings.storage.memory import Storage


class _Data:
    def __init__(self) -> None:
        self.has_completed = False
        self.has_scheduled = False


class LatestSeasonWeekQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(
        self,
        query: LatestSeasonWeekQuery,
    ) -> LatestSeasonWeekResult:
        for season in sorted(
            self._storage.season.all_(),
            key=lambda s: s.year,
            reverse=True,
        ):
            season_data = _Data()
            weeks: dict[int, _Data] = {}
            for game in self._storage.game.for_season(season.id_):
                week_data = weeks.setdefault(game.week, _Data())
                if game.status == GameStatus.GAME_STATUS_COMPLETED:
                    season_data.has_completed = True
                    week_data.has_completed = True
                elif game.status == GameStatus.GAME_STATUS_SCHEDULED:
                    season_data.has_scheduled = True
                    week_data.has_scheduled = True

            if season_data.has_scheduled is False and season_data.has_completed is True:
                return LatestSeasonWeekResult(
                    query_id=query.query_id,
                    latest=LatestSeasonWeekValue(
                        season_id=str(season.id_),
                        year=season.year,
                        week=None,
                    ),
                )

            completed_weeks: list[int] = []
            for week, data in weeks.items():
                if data.has_scheduled is False and data.has_completed is True:
                    completed_weeks.append(week)
            if len(completed_weeks) > 0:
                sorted_weeks = sorted(completed_weeks, reverse=True)
                return LatestSeasonWeekResult(
                    query_id=query.query_id,
                    latest=LatestSeasonWeekValue(
                        season_id=str(season.id_),
                        year=season.year,
                        week=sorted_weeks[0],
                    ),
                )

        return LatestSeasonWeekResult(query_id=query.query_id, latest=None)
