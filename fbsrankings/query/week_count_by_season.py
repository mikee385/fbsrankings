from uuid import UUID

from fbsrankings.common import Query


class WeekCountBySeasonResult(object):
    def __init__(self, season_ID: UUID, count: int) -> None:
        self.season_ID = season_ID
        self.count = count


class WeekCountBySeasonQuery(Query[WeekCountBySeasonResult]):
    def __init__(self, season_ID: UUID) -> None:
        self.season_ID = season_ID
