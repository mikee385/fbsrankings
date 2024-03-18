from typing import Dict
from uuid import UUID

from fbsrankings.enum import GameStatus
from fbsrankings.ranking.command.domain.model.core import SeasonID
from fbsrankings.ranking.command.domain.model.core import TeamID
from fbsrankings.ranking.command.domain.model.ranking import Ranking
from fbsrankings.ranking.command.domain.model.ranking import SeasonData
from fbsrankings.ranking.command.domain.model.ranking import TeamRankingCalculator
from fbsrankings.ranking.command.domain.model.ranking import TeamRankingRepository


class TeamData:
    def __init__(self) -> None:
        self.game_total = 0
        self.opponent_sum = 0.0

    def add_opponent(self, opponent_value: float) -> None:
        self.game_total += 1
        self.opponent_sum += opponent_value

    @property
    def strength_of_schedule(self) -> float:
        return self.opponent_sum / self.game_total if self.game_total > 0 else 0.0


class StrengthOfScheduleRankingCalculator:
    def __init__(self, repository: TeamRankingRepository) -> None:
        self._repository = repository

    def calculate_for_ranking(
        self,
        season_data: SeasonData,
        performance_ranking: Ranking[TeamID],
    ) -> Ranking[TeamID]:
        team_data: Dict[UUID, TeamData] = {}

        performance_map = {r.id_: r for r in performance_ranking.values}

        for game in season_data.game_map.values():
            if game.status != GameStatus.CANCELED.name:
                home_performance = performance_map.get(TeamID(game.home_team_id))
                away_performance = performance_map.get(TeamID(game.away_team_id))

                if home_performance is not None and away_performance is not None:
                    home_data = team_data.get(game.home_team_id)
                    if home_data is None:
                        home_data = TeamData()
                        team_data[game.home_team_id] = home_data
                    home_data.add_opponent(away_performance.value)

                    away_data = team_data.get(game.away_team_id)
                    if away_data is None:
                        away_data = TeamData()
                        team_data[game.away_team_id] = away_data
                    away_data.add_opponent(home_performance.value)

        result = {
            TeamID(id_): data.strength_of_schedule for id_, data in team_data.items()
        }
        ranking_values = TeamRankingCalculator.to_values(season_data, result)

        return self._repository.create(
            performance_ranking.name + " - Strength of Schedule - Total",
            SeasonID(season_data.season_id),
            performance_ranking.week,
            ranking_values,
        )
