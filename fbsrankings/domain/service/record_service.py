from typing import Dict
from typing import List

from fbsrankings.domain.model.affiliation import Subdivision
from fbsrankings.domain.model.game import Game
from fbsrankings.domain.model.game import GameStatus
from fbsrankings.domain.model.ranking import SeasonData
from fbsrankings.domain.model.record import TeamRecord
from fbsrankings.domain.model.record import TeamRecordRepository
from fbsrankings.domain.model.record import TeamRecordValue
from fbsrankings.domain.model.team import TeamID


class TeamData:
    def __init__(self) -> None:
        self.wins = 0
        self.losses = 0


class TeamRecordService:
    def __init__(self, repository: TeamRecordRepository) -> None:
        self._repository = repository

    def calculate_for_season(self, season_data: SeasonData) -> List[TeamRecord]:
        team_data: Dict[TeamID, TeamData] = {}
        for affiliation in season_data.affiliation_map.values():
            if affiliation.subdivision == Subdivision.FBS:
                team_data[affiliation.team_id] = TeamData()

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

        records = []
        for week in sorted(games_by_week.keys()):
            for game in games_by_week[week]:
                if game.winning_team_id is not None and game.losing_team_id is not None:
                    winning_data = team_data[game.winning_team_id]
                    losing_data = team_data[game.losing_team_id]

                    winning_data.wins += 1
                    losing_data.losses += 1

            record_values = [
                TeamRecordValue(id, data.wins, data.losses)
                for id, data in team_data.items()
            ]

            records.append(
                self._repository.create(season_data.season.id, week, record_values),
            )

        if season_is_complete:
            records.append(
                self._repository.create(season_data.season.id, None, record_values),
            )

        return records
