from typing import Dict
from typing import List

import numpy

from fbsrankings.domain.model.affiliation import Subdivision
from fbsrankings.domain.model.game import Game
from fbsrankings.domain.model.game import GameStatus
from fbsrankings.domain.model.ranking import Ranking
from fbsrankings.domain.model.ranking import SeasonData
from fbsrankings.domain.model.ranking import TeamRankingRepository
from fbsrankings.domain.model.ranking import TeamRankingService
from fbsrankings.domain.model.season import SeasonID
from fbsrankings.domain.model.team import TeamID


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


class ColleyMatrixRankingService(TeamRankingService):
    name: str = "Colley Matrix"

    def __init__(self, repository: TeamRankingRepository) -> None:
        self._repository = repository

    def calculate_for_season(
        self, season_ID: SeasonID, season_data: SeasonData
    ) -> List[Ranking[TeamID]]:
        team_data: Dict[TeamID, TeamData] = {}
        for affiliation in season_data.affiliation_map.values():
            if affiliation.subdivision == Subdivision.FBS:
                team_data[affiliation.team_ID] = TeamData(len(team_data))

        season_is_complete = True
        games_by_week: Dict[int, List[Game]] = {}
        for game in season_data.game_map.values():
            winning_data = None
            if game.winning_team_ID is not None:
                winning_data = team_data.get(game.winning_team_ID)

            losing_data = None
            if game.losing_team_ID is not None:
                losing_data = team_data.get(game.losing_team_ID)

            if winning_data is not None and losing_data is not None:
                week_games = games_by_week.setdefault(game.week, [])
                week_games.append(game)

            elif game.status == GameStatus.SCHEDULED:
                season_is_complete = False

        n = len(team_data)
        a = numpy.zeros((n, n))
        b = numpy.zeros(n)

        rankings = []
        for week in sorted(games_by_week.keys()):
            for game in games_by_week[week]:
                if game.winning_team_ID is not None and game.losing_team_ID is not None:
                    winning_data = team_data[game.winning_team_ID]
                    losing_data = team_data[game.losing_team_ID]

                    winning_data.add_win()
                    losing_data.add_loss()

                    a[winning_data.index, losing_data.index] -= 1.0
                    a[losing_data.index, winning_data.index] -= 1.0

            for data in team_data.values():
                a[data.index, data.index] = 2.0 + data.game_total
                b[data.index] = 1 + (data.win_total - data.loss_total) / 2.0

            x = numpy.linalg.solve(a, b)

            result = {ID: x[data.index] for ID, data in team_data.items()}
            ranking_values = TeamRankingService._to_values(season_data, result)

            rankings.append(
                self._repository.create(
                    ColleyMatrixRankingService.name, season_ID, week, ranking_values,
                )
            )

        if season_is_complete:
            rankings.append(
                self._repository.create(
                    ColleyMatrixRankingService.name, season_ID, None, ranking_values,
                )
            )

        return rankings
