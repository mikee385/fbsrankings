from fbsrankings.core.query.query.team_count_by_season import TeamCountBySeasonQuery
from fbsrankings.core.query.query.team_count_by_season import TeamCountBySeasonResult
from fbsrankings.storage.memory import Storage


class TeamCountBySeasonQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: TeamCountBySeasonQuery) -> TeamCountBySeasonResult:
        return TeamCountBySeasonResult(
            query.season_id,
            len(self._storage.affiliation.for_season(query.season_id)),
        )
