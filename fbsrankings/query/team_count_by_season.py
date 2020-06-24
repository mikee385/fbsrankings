from uuid import UUID

from fbsrankings.common import Query


class TeamCountBySeasonResult(object):
    def __init__(self, season_ID: UUID, count: int) -> None:
        self.season_ID = season_ID
        self.count = count


class TeamCountBySeasonQuery(Query[TeamCountBySeasonResult]):
    def __init__(self, season_ID: UUID) -> None:
        self.season_ID = season_ID
