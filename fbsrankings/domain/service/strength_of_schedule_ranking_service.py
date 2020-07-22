from typing import Dict

from fbsrankings.domain.model.ranking import Ranking
from fbsrankings.domain.model.ranking import SeasonData
from fbsrankings.domain.model.ranking import TeamRankingRepository
from fbsrankings.domain.model.ranking import TeamRankingService
from fbsrankings.domain.model.team import TeamID


class TeamData(object):
    def __init__(self) -> None:
        self.game_total = 0
        self.opponent_sum = 0.0

    def add_opponent(self, opponent_value: float) -> None:
        self.game_total += 1
        self.opponent_sum += opponent_value

    @property
    def strength_of_schedule(self) -> float:
        return self.opponent_sum / self.game_total if self.game_total > 0 else 0.0


class StrengthOfScheduleRankingService(TeamRankingService):
    def __init__(self, repository: TeamRankingRepository) -> None:
        self._repository = repository

    def calculate_for_ranking(
        self, season_data: SeasonData, performance_ranking: Ranking[TeamID]
    ) -> Ranking[TeamID]:
        team_data: Dict[TeamID, TeamData] = {}

        performance_map = {r.ID: r for r in performance_ranking.values}

        for game in season_data.game_map.values():
            home_performance = performance_map.get(game.home_team_ID)
            away_performance = performance_map.get(game.away_team_ID)

            if home_performance is not None and away_performance is not None:
                home_data = team_data.get(game.home_team_ID)
                if home_data is None:
                    home_data = TeamData()
                    team_data[game.home_team_ID] = home_data
                home_data.add_opponent(away_performance.value)

                away_data = team_data.get(game.away_team_ID)
                if away_data is None:
                    away_data = TeamData()
                    team_data[game.away_team_ID] = away_data
                away_data.add_opponent(home_performance.value)

        result = {ID: data.strength_of_schedule for ID, data in team_data.items()}
        ranking_values = TeamRankingService._to_values(season_data, result)

        return self._repository.create(
            performance_ranking.name + " - Strength of Schedule - Total",
            season_data.season.ID,
            performance_ranking.week,
            ranking_values,
        )
