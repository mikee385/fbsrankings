from typing import Optional

from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.query import GameRankingBySeasonWeekQuery
from fbsrankings.query import GameRankingBySeasonWeekResult
from fbsrankings.query import GameRankingValueBySeasonWeekResult


class GameRankingBySeasonWeekQueryHandler(object):
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(
        self, query: GameRankingBySeasonWeekQuery
    ) -> Optional[GameRankingBySeasonWeekResult]:
        ranking = self._storage.game_ranking.find(
            query.name, query.season_ID, query.week
        )
        if ranking is not None:
            season = self._storage.season.get(ranking.season_ID)
            if season is not None:

                values = []
                for value in ranking.values:
                    game = self._storage.game.get(value.ID)

                    if game is not None:
                        home_team = self._storage.team.get(game.home_team_ID)
                        away_team = self._storage.team.get(game.away_team_ID)

                        if home_team is not None and away_team is not None:
                            values.append(
                                GameRankingValueBySeasonWeekResult(
                                    game.ID,
                                    game.season_ID,
                                    season.year,
                                    game.week,
                                    game.date,
                                    game.season_section,
                                    game.home_team_ID,
                                    home_team.name,
                                    game.away_team_ID,
                                    away_team.name,
                                    game.home_team_score,
                                    game.away_team_score,
                                    game.status,
                                    game.notes,
                                    value.order,
                                    value.rank,
                                    value.value,
                                )
                            )

                return GameRankingBySeasonWeekResult(
                    ranking.ID,
                    ranking.name,
                    ranking.season_ID,
                    season.year,
                    ranking.week,
                    values,
                )
            else:
                return None
        else:
            return None
