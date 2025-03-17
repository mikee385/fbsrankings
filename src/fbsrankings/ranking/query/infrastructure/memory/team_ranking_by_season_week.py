from typing import Optional

from fbsrankings.messages.query import TeamRankingBySeasonWeekQuery
from fbsrankings.messages.query import TeamRankingBySeasonWeekResult
from fbsrankings.messages.query import TeamRankingValueBySeasonWeekResult
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
            query.week if query.HasField("week") else None,
        )
        if ranking is not None:
            season = self._storage.season.get(ranking.season_id)

            values = []
            for value in ranking.values:
                team = self._storage.team.get(value.id_)
                if team is not None:
                    values.append(
                        TeamRankingValueBySeasonWeekResult(
                            team_id=value.id_,
                            name=team.name,
                            order=value.order,
                            rank=value.rank,
                            value=value.value,
                        ),
                    )

            if season is not None:
                return TeamRankingBySeasonWeekResult(
                    ranking_id=str(ranking.id_),
                    name=ranking.name,
                    season_id=str(ranking.season_id),
                    year=season.year,
                    week=ranking.week,
                    values=values,
                )
        return None
