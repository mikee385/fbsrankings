from fbsrankings.messages.query import TeamCountBySeasonQuery
from fbsrankings.messages.query import TeamCountBySeasonResult
from fbsrankings.storage.memory import Storage


class TeamCountBySeasonQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: TeamCountBySeasonQuery) -> TeamCountBySeasonResult:
        return TeamCountBySeasonResult(
            query_id=query.query_id,
            season_id=query.season_id,
            count=len(self._storage.affiliation.for_season(query.season_id)),
        )
