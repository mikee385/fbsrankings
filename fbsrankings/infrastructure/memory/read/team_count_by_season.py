from fbsrankings.common import QueryHandler
from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.query import TeamCountBySeasonQuery, TeamCountBySeasonResult


class TeamCountBySeasonQueryHandler(
    QueryHandler[TeamCountBySeasonQuery, TeamCountBySeasonResult]
):
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def handle(self, query: TeamCountBySeasonQuery) -> TeamCountBySeasonResult:
        return TeamCountBySeasonResult(
            query.season_ID, len(self._storage.affiliation.by_season(query.season_ID))
        )
