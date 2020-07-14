from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.query import TeamRankingBySeasonWeekQuery
from fbsrankings.query import TeamRankingBySeasonWeekResult
from fbsrankings.query import TeamRankingValueBySeasonWeekResult


class TeamRankingBySeasonWeekQueryHandler(object):
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: TeamRankingBySeasonWeekQuery) -> TeamRankingBySeasonWeekResult:
        ranking = self._storage.team_ranking.find(query.name, query.season_ID, query.week)
        if ranking is not None:
            season = self._storage.season.get(ranking.season_ID)
            
            values = []
            for value in ranking.values:
                team = self._storage.team.get(value.ID)
                if team is not None:
                    values.append(TeamRankingValueBySeasonWeekResult(value.ID, team.name, value.order, value.rank, value.value))
            
            if season is not None:
                return TeamRankingBySeasonWeekResult(ranking.ID, ranking.name, ranking.season_ID, season.year, ranking.week, values)
            else:
                return None
        else:
            return None

