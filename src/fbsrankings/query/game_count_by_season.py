from uuid import UUID

from fbsrankings.common import Query


class GameCountBySeasonResult:
    def __init__(self, season_id: UUID, count: int) -> None:
        self.season_id = season_id
        self.count = count


class GameCountBySeasonQuery(Query[GameCountBySeasonResult]):
    def __init__(self, season_id: UUID) -> None:
        self.season_id = season_id
