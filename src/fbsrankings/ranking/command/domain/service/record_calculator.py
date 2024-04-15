from typing import Dict
from typing import List
from uuid import UUID

from fbsrankings.core.query import GameBySeasonResult
from fbsrankings.enum import GameStatus
from fbsrankings.enum import Subdivision
from fbsrankings.ranking.command.domain.model.core import SeasonID
from fbsrankings.ranking.command.domain.model.core import TeamID
from fbsrankings.ranking.command.domain.model.ranking import SeasonData
from fbsrankings.ranking.command.domain.model.record import TeamRecord
from fbsrankings.ranking.command.domain.model.record import TeamRecordFactory
from fbsrankings.ranking.command.domain.model.record import TeamRecordValue


class TeamData:
    def __init__(self) -> None:
        self.wins = 0
        self.losses = 0


class TeamRecordCalculator:
    def __init__(self, factory: TeamRecordFactory) -> None:
        self._factory = factory

    def calculate_for_season(self, season_data: SeasonData) -> List[TeamRecord]:
        team_data: Dict[UUID, TeamData] = {}
        for affiliation in season_data.affiliation_map.values():
            if affiliation.subdivision == Subdivision.FBS.name:
                team_data[affiliation.team_id] = TeamData()

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

        records = []
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
                    winning_data.wins += 1
                    losing_data.losses += 1

            record_values = [
                TeamRecordValue(TeamID(id_), data.wins, data.losses)
                for id_, data in team_data.items()
            ]

            records.append(
                self._factory.create(
                    SeasonID(season_data.season_id),
                    week,
                    record_values,
                ),
            )

        if season_is_complete:
            records.append(
                self._factory.create(
                    SeasonID(season_data.season_id),
                    None,
                    record_values,
                ),
            )

        return records
