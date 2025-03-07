from typing import Dict
from uuid import UUID

from fbsrankings.messages.enums import GameStatus
from fbsrankings.ranking.command.domain.model.core import GameID
from fbsrankings.ranking.command.domain.model.core import SeasonID
from fbsrankings.ranking.command.domain.model.core import TeamID
from fbsrankings.ranking.command.domain.model.ranking import GameRankingCalculator
from fbsrankings.ranking.command.domain.model.ranking import GameRankingFactory
from fbsrankings.ranking.command.domain.model.ranking import Ranking
from fbsrankings.ranking.command.domain.model.ranking import SeasonData


class GameStrengthRankingCalculator:
    def __init__(self, factory: GameRankingFactory) -> None:
        self._factory = factory

    def calculate_for_ranking(
        self,
        season_data: SeasonData,
        performance_ranking: Ranking[TeamID],
    ) -> Ranking[GameID]:
        game_data: Dict[UUID, float] = {}

        performance_map = {r.id_: r for r in performance_ranking.values}

        for game in season_data.game_map.values():
            if game.status != GameStatus.CANCELED.name:
                home_performance = performance_map.get(TeamID(UUID(game.home_team_id)))
                away_performance = performance_map.get(TeamID(UUID(game.away_team_id)))

                if home_performance is not None and away_performance is not None:
                    if home_performance.value > away_performance.value:
                        game_value = (
                            99 * away_performance.value + home_performance.value
                        ) / 100.0
                    else:
                        game_value = (
                            99 * home_performance.value + away_performance.value
                        ) / 100.0
                    game_data[UUID(game.game_id)] = game_value

        result = {GameID(id_): data for id_, data in game_data.items()}
        ranking_values = GameRankingCalculator.to_values(season_data, result)

        return self._factory.create(
            performance_ranking.name + " - Game Strength",
            SeasonID(season_data.season_id),
            performance_ranking.week,
            ranking_values,
        )
