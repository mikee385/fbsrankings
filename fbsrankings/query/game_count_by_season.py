from uuid import UUID

from fbsrankings.common import Query


class GameCountBySeasonResult(object):
    def __init__(self, season_ID: UUID, count: int) -> None:
        self.season_ID = season_ID
        self.count = count


class GameCountBySeasonQuery(Query[GameCountBySeasonResult]):
    def __init__(self, season_ID: UUID) -> None:
        self.season_ID = season_ID
