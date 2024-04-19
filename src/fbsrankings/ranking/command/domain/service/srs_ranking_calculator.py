from typing import Dict
from typing import List
from uuid import UUID

import numpy

from fbsrankings.core.query import GameBySeasonResult
from fbsrankings.enums import GameStatus
from fbsrankings.enums import Subdivision
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
        self.point_margin = 0

    def add_game(self, point_margin: int) -> None:
        self.game_total += 1
        self.point_margin += point_margin


class SRSRankingCalculator:
    name: str = "SRS"

    def __init__(self, factory: TeamRankingFactory) -> None:
        self._factory = factory

    def calculate_for_season(self, season_data: SeasonData) -> List[Ranking[TeamID]]:
        team_data: Dict[UUID, TeamData] = {}
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
        a = numpy.zeros((n + 1, n))
        b = numpy.zeros(n + 1)

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
                a[data.index, data.index] = data.game_total
                b[data.index] = data.point_margin
                a[n, data.index] = 1.0
            b[n] = 0.0

            x = numpy.linalg.lstsq(a, b, rcond=-1)[0]

            result = {TeamID(id_): x[data.index] for id_, data in team_data.items()}
            ranking_values = TeamRankingCalculator.to_values(season_data, result)

            rankings.append(
                self._factory.create(
                    SRSRankingCalculator.name,
                    SeasonID(season_data.season_id),
                    week,
                    ranking_values,
                ),
            )

        if season_is_complete:
            rankings.append(
                self._factory.create(
                    SRSRankingCalculator.name,
                    SeasonID(season_data.season_id),
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
