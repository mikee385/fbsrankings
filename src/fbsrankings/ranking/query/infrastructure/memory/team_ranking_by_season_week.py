from typing import Optional

from fbsrankings.shared.query import TeamRankingBySeasonWeekQuery
from fbsrankings.shared.query import TeamRankingBySeasonWeekResult
from fbsrankings.shared.query import TeamRankingValueBySeasonWeekResult
from fbsrankings.storage.memory import Storage


class TeamRankingBySeasonWeekQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(
        self,
        query: TeamRankingBySeasonWeekQuery,
    ) -> Optional[TeamRankingBySeasonWeekResult]:
        ranking = self._storage.team_ranking.find(
            query.name,
            query.season_id,
            query.week,
        )
        if ranking is not None:
            season = self._storage.season.get(ranking.season_id)

            values = []
            for value in ranking.values:
                team = self._storage.team.get(value.id_)
                if team is not None:
                    values.append(
                        TeamRankingValueBySeasonWeekResult(
                            value.id_,
                            team.name,
                            value.order,
                            value.rank,
                            value.value,
                        ),
                    )

            if season is not None:
                return TeamRankingBySeasonWeekResult(
                    ranking.id_,
                    ranking.name,
                    ranking.season_id,
                    season.year,
                    ranking.week,
                    values,
                )
        return None
