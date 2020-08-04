from uuid import UUID

from fbsrankings.common import Query


class WeekCountBySeasonResult(object):
    def __init__(self, season_id: UUID, count: int) -> None:
        self.season_id = season_id
        self.count = count


class WeekCountBySeasonQuery(Query[WeekCountBySeasonResult]):
    def __init__(self, season_id: UUID) -> None:
        self.season_id = season_id
