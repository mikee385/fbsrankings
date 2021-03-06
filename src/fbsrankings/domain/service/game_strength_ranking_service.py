from typing import Dict

from fbsrankings.domain.model.game import GameID
from fbsrankings.domain.model.game import GameStatus
from fbsrankings.domain.model.ranking import GameRankingRepository
from fbsrankings.domain.model.ranking import GameRankingService
from fbsrankings.domain.model.ranking import Ranking
from fbsrankings.domain.model.ranking import SeasonData
from fbsrankings.domain.model.team import TeamID


class GameStrengthRankingService(GameRankingService):
    def __init__(self, repository: GameRankingRepository) -> None:
        self._repository = repository

    def calculate_for_ranking(
        self, season_data: SeasonData, performance_ranking: Ranking[TeamID],
    ) -> Ranking[GameID]:
        game_data: Dict[GameID, float] = {}

        performance_map = {r.id_: r for r in performance_ranking.values}

        for game in season_data.game_map.values():
            if game.status != GameStatus.CANCELED:
                home_performance = performance_map.get(game.home_team_id)
                away_performance = performance_map.get(game.away_team_id)

                if home_performance is not None and away_performance is not None:
                    if home_performance.value > away_performance.value:
                        game_value = (
                            99 * away_performance.value + home_performance.value
                        ) / 100.0
                    else:
                        game_value = (
                            99 * home_performance.value + away_performance.value
                        ) / 100.0
                    game_data[game.id_] = game_value

        ranking_values = GameRankingService._to_values(season_data, game_data)

        return self._repository.create(
            performance_ranking.name + " - Game Strength",
            season_data.season.id_,
            performance_ranking.week,
            ranking_values,
        )
