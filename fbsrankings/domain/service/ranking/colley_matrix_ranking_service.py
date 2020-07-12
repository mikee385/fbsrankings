from typing import Dict
from typing import List

import numpy

from fbsrankings.domain.model.affiliation import Subdivision
from fbsrankings.domain.model.game import Game
from fbsrankings.domain.model.game import GameStatus
from fbsrankings.domain.model.ranking import Ranking
from fbsrankings.domain.model.ranking import RankingRepository
from fbsrankings.domain.model.ranking import RankingService
from fbsrankings.domain.model.ranking import RankingType
from fbsrankings.domain.model.ranking import SeasonData
from fbsrankings.domain.model.season import SeasonID
from fbsrankings.domain.model.season import SeasonSection
from fbsrankings.domain.model.team import TeamID
from fbsrankings.domain.service.ranking.helper import TeamValueHelper


class TeamData(object):
    def __init__(self, index: int) -> None:
        self.index = index
        self.game_total = 0
        self.win_total = 0
        self.loss_total = 0

    def add_win(self) -> None:
        self.game_total += 1
        self.win_total += 1

    def add_loss(self) -> None:
        self.game_total += 1
        self.loss_total += 1


class ColleyMatrixRankingService(RankingService[TeamID]):
    name: str = "Colley Matrix"

    def __init__(self, repository: RankingRepository) -> None:
        self._repository = repository

    def calculate_for_season(
        self, season_ID: SeasonID, season_data: SeasonData
    ) -> List[Ranking[TeamID]]:
        team_data: Dict[TeamID, TeamData] = {}
        fbs_games: List[Game] = []

        for game in season_data.games:
            home_affiliation = season_data.affiliation_map[game.home_team_ID]
            away_affiliation = season_data.affiliation_map[game.away_team_ID]

            if (
                game.season_section == SeasonSection.REGULAR_SEASON
                and game.status == GameStatus.COMPLETED
                and home_affiliation.subdivision == Subdivision.FBS
                and away_affiliation.subdivision == Subdivision.FBS
            ):
                if game.winning_team_ID is not None:
                    winning_data = team_data.get(game.winning_team_ID)
                    if winning_data is None:
                        winning_data = TeamData(len(team_data))
                        team_data[game.winning_team_ID] = winning_data
                    winning_data.add_win()

                if game.losing_team_ID is not None:
                    losing_data = team_data.get(game.losing_team_ID)
                    if losing_data is None:
                        losing_data = TeamData(len(team_data))
                        team_data[game.losing_team_ID] = losing_data
                    losing_data.add_loss()

                fbs_games.append(game)

        n = len(team_data)
        a = numpy.zeros((n, n))
        b = numpy.zeros(n)

        for _, data in team_data.items():
            index = data.index
            a[index, index] = 2.0 + data.game_total
            b[index] = 1 + (data.win_total - data.loss_total) / 2.0

        for game in fbs_games:
            if game.winning_team_ID is not None and game.losing_team_ID is not None:
                winning_data = team_data[game.winning_team_ID]
                losing_data = team_data[game.losing_team_ID]

                a[winning_data.index, losing_data.index] -= 1.0
                a[losing_data.index, winning_data.index] -= 1.0

        x = numpy.linalg.solve(a, b)

        result: Dict[TeamID, float] = {}
        for ID, data in team_data.items():
            result[ID] = x[data.index]

        helper = TeamValueHelper(season_data)
        ranking_values = helper.to_values(result)

        return [
            self._repository.create(
                ColleyMatrixRankingService.name,
                RankingType.TEAM,
                season_ID,
                None,
                ranking_values,
            )
        ]
