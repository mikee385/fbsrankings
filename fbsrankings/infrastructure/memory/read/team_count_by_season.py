from fbsrankings.common import Query, QueryHandler
from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.query import TeamCountBySeasonQuery, TeamCountBySeasonResult


class TeamCountBySeasonQueryHandler (QueryHandler):
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def handle(self, query: Query) -> TeamCountBySeasonResult:
        if not isinstance(query, TeamCountBySeasonQuery):
            raise TypeError('query must be of type TeamCountBySeasonQuery')
        
        return TeamCountBySeasonResult(query.season_ID, len(self._storage.affiliation.by_season(query.season_ID)))
