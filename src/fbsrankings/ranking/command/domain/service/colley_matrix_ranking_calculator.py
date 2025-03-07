from typing import Dict
from typing import List
from uuid import UUID

import numpy

from fbsrankings.messages.enums import GameStatus
from fbsrankings.messages.enums import Subdivision
from fbsrankings.messages.query import GameBySeasonResult
from fbsrankings.ranking.command.domain.model.core import SeasonID
from fbsrankings.ranking.command.domain.model.core import TeamID
from fbsrankings.ranking.command.domain.model.ranking import Ranking
from fbsrankings.ranking.command.domain.model.ranking import SeasonData
from fbsrankings.ranking.command.domain.model.ranking import TeamRankingCalculator
from fbsrankings.ranking.command.domain.model.ranking import TeamRankingFactory


class TeamData:
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


class ColleyMatrixRankingCalculator:
    name: str = "Colley Matrix"

    def __init__(self, factory: TeamRankingFactory) -> None:
        self._factory = factory

    def calculate_for_season(self, season_data: SeasonData) -> List[Ranking[TeamID]]:
        team_data: Dict[str, TeamData] = {}
        for affiliation in season_data.affiliation_map.values():
            if affiliation.subdivision == Subdivision.FBS.name:
                team_data[affiliation.team_id] = TeamData(len(team_data))

        season_is_complete = True
        games_by_week: Dict[int, List[GameBySeasonResult]] = {}
        for game in season_data.game_map.values():
            winning_data = None
            losing_data = None

            if game.home_team_score is not None and game.away_team_score is not None:
                if game.home_team_score > game.away_team_score:
                    winning_data = team_data.get(game.home_team_id)
                    losing_data = team_data.get(game.away_team_id)
                elif game.away_team_score > game.home_team_score:
                    winning_data = team_data.get(game.away_team_id)
                    losing_data = team_data.get(game.home_team_id)

            if winning_data is not None and losing_data is not None:
                week_games = games_by_week.setdefault(game.week, [])
                week_games.append(game)

            elif game.status == GameStatus.SCHEDULED.name:
                season_is_complete = False

        n = len(team_data)
        a = numpy.zeros((n, n))
        b = numpy.zeros(n)

        rankings = []
        for week in sorted(games_by_week.keys()):
            for game in games_by_week[week]:
                winning_data = None
                losing_data = None

                if (
                    game.home_team_score is not None
                    and game.away_team_score is not None
                ):
                    if game.home_team_score > game.away_team_score:
                        winning_data = team_data.get(game.home_team_id)
                        losing_data = team_data.get(game.away_team_id)
                    elif game.away_team_score > game.home_team_score:
                        winning_data = team_data.get(game.away_team_id)
                        losing_data = team_data.get(game.home_team_id)

                if winning_data is not None and losing_data is not None:
                    winning_data.add_win()
                    losing_data.add_loss()

                    a[winning_data.index, losing_data.index] -= 1.0
                    a[losing_data.index, winning_data.index] -= 1.0

            for data in team_data.values():
                a[data.index, data.index] = 2.0 + data.game_total
                b[data.index] = 1 + (data.win_total - data.loss_total) / 2.0

            x = numpy.linalg.solve(a, b)

            result = {
                TeamID(UUID(id_)): x[data.index] for id_, data in team_data.items()
            }
            ranking_values = TeamRankingCalculator.to_values(season_data, result)

            rankings.append(
                self._factory.create(
                    ColleyMatrixRankingCalculator.name,
                    SeasonID(season_data.season_id),
                    week,
                    ranking_values,
                ),
            )

        if season_is_complete:
            rankings.append(
                self._factory.create(
                    ColleyMatrixRankingCalculator.name,
                    SeasonID(season_data.season_id),
                    None,
                    ranking_values,
                ),
            )

        return rankings
