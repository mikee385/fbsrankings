import sys
from typing import Dict

from fbsrankings.domain.model.game import GameID
from fbsrankings.domain.model.ranking import GameRankingRepository
from fbsrankings.domain.model.ranking import GameRankingService
from fbsrankings.domain.model.ranking import Ranking
from fbsrankings.domain.model.ranking import SeasonData
from fbsrankings.domain.model.team import TeamID


class GameData(object):
    def __init__(self) -> None:
        self.min_team_value = sys.float_info.max

    def add_team(self, team_value: float) -> None:
        self.min_team_value = min(self.min_team_value, team_value)

    @property
    def game_value(self) -> float:
        return self.min_team_value


class GameStrengthRankingService(GameRankingService):
    def __init__(self, repository: GameRankingRepository) -> None:
        self._repository = repository

    def calculate_for_ranking(
        self, season_data: SeasonData, performance_ranking: Ranking[TeamID]
    ) -> Ranking[GameID]:
        game_data: Dict[GameID, GameData] = {}

        performance_map = {r.ID: r for r in performance_ranking.values}

        for game in season_data.game_map.values():
            home_performance = performance_map.get(game.home_team_ID)
            away_performance = performance_map.get(game.away_team_ID)

            if home_performance is not None and away_performance is not None:
                data = GameData()
                data.add_team(home_performance.value)
                data.add_team(away_performance.value)
                game_data[game.ID] = data

        result = {ID: data.game_value for ID, data in game_data.items()}
        ranking_values = GameRankingService._to_values(season_data, result)

        return self._repository.create(
            performance_ranking.name + " - Game Strength",
            season_data.season.ID,
            performance_ranking.week,
            ranking_values,
        )
