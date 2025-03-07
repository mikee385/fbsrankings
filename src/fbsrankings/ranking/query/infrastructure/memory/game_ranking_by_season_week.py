from typing import Optional

from fbsrankings.messages.query import GameRankingBySeasonWeekQuery
from fbsrankings.messages.query import GameRankingBySeasonWeekResult
from fbsrankings.messages.query import GameRankingValueBySeasonWeekResult
from fbsrankings.storage.memory import Storage


class GameRankingBySeasonWeekQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(
        self,
        query: GameRankingBySeasonWeekQuery,
    ) -> Optional[GameRankingBySeasonWeekResult]:
        ranking = self._storage.game_ranking.find(
            query.name,
            query.season_id,
            query.week,
        )
        if ranking is not None:
            season = self._storage.season.get(ranking.season_id)
            if season is not None:
                values = []
                for value in ranking.values:
                    game = self._storage.game.get(value.id_)

                    if game is not None:
                        home_team = self._storage.team.get(game.home_team_id)
                        away_team = self._storage.team.get(game.away_team_id)

                        if home_team is not None and away_team is not None:
                            values.append(
                                GameRankingValueBySeasonWeekResult(
                                    str(game.id_),
                                    str(game.season_id),
                                    season.year,
                                    game.week,
                                    game.date,
                                    game.season_section,
                                    str(game.home_team_id),
                                    home_team.name,
                                    str(game.away_team_id),
                                    away_team.name,
                                    game.home_team_score,
                                    game.away_team_score,
                                    game.status,
                                    game.notes,
                                    value.order,
                                    value.rank,
                                    value.value,
                                ),
                            )

                return GameRankingBySeasonWeekResult(
                    str(ranking.id_),
                    ranking.name,
                    str(ranking.season_id),
                    season.year,
                    ranking.week,
                    values,
                )
        return None
