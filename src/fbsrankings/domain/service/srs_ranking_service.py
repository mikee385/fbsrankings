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
from fbsrankings.domain.model.team import TeamID


class TeamData:
    def __init__(self, index: int) -> None:
        self.index = index
        self.game_total = 0
        self.point_margin = 0

    def add_game(self, point_margin: int) -> None:
        self.game_total += 1
        self.point_margin += point_margin


class SRSRankingService(TeamRankingService):
    name: str = "SRS"

    def __init__(self, repository: TeamRankingRepository) -> None:
        self._repository = repository

    def calculate_for_season(self, season_data: SeasonData) -> List[Ranking[TeamID]]:
        team_data: Dict[TeamID, TeamData] = {}
        for affiliation in season_data.affiliation_map.values():
            if affiliation.subdivision == Subdivision.FBS:
                team_data[affiliation.team_id] = TeamData(len(team_data))

        season_is_complete = True
        games_by_week: Dict[int, List[Game]] = {}
        for game in season_data.game_map.values():
            winning_data = None
            if game.winning_team_id is not None:
                winning_data = team_data.get(game.winning_team_id)

            losing_data = None
            if game.losing_team_id is not None:
                losing_data = team_data.get(game.losing_team_id)

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
                if (
                    game.home_team_score is not None
                    and game.away_team_score is not None
                ):
                    home_data = team_data[game.home_team_id]
                    away_data = team_data[game.away_team_id]

                    home_margin = self._adjust_margin(
                        game.home_team_score - game.away_team_score,
                    )
                    home_data.add_game(home_margin)
                    away_data.add_game(-home_margin)

                    a[home_data.index, away_data.index] -= 1.0
                    a[away_data.index, home_data.index] -= 1.0

            for data in team_data.values():
                a[data.index, data.index] = max(data.game_total, 1.0)
                b[data.index] = data.point_margin

            try:
                x = numpy.linalg.solve(a, b)
            except numpy.linalg.LinAlgError as error:
                if str(error) == "Singular matrix":
                    continue
                raise

            shift = numpy.sum(x) / n
            x -= shift

            result = {id_: x[data.index] for id_, data in team_data.items()}
            ranking_values = TeamRankingService._to_values(season_data, result)

            rankings.append(
                self._repository.create(
                    SRSRankingService.name,
                    season_data.season.id_,
                    week,
                    ranking_values,
                ),
            )

        if season_is_complete:
            rankings.append(
                self._repository.create(
                    SRSRankingService.name,
                    season_data.season.id_,
                    None,
                    ranking_values,
                ),
            )

        return rankings

    @staticmethod
    def _adjust_margin(margin: int) -> int:
        if margin > 24:
            return 24
        if margin < -24:
            return -24
        if 0 < margin < 7:
            return 7
        if 0 > margin > -7:
            return -7
        return margin
