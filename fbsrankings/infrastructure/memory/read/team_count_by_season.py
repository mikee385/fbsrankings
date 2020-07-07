from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.query import TeamCountBySeasonQuery
from fbsrankings.query import TeamCountBySeasonResult


class TeamCountBySeasonQueryHandler(object):
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: TeamCountBySeasonQuery) -> TeamCountBySeasonResult:
        return TeamCountBySeasonResult(
            query.season_ID, len(self._storage.affiliation.for_season(query.season_ID))
        )
