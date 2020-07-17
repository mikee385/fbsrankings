from typing import Dict
from typing import List

from fbsrankings.domain.model.affiliation import Subdivision
from fbsrankings.domain.model.game import GameStatus
from fbsrankings.domain.model.ranking import SeasonData
from fbsrankings.domain.model.record import TeamRecord
from fbsrankings.domain.model.record import TeamRecordRepository
from fbsrankings.domain.model.record import TeamRecordValue
from fbsrankings.domain.model.season import SeasonID
from fbsrankings.domain.model.season import SeasonSection
from fbsrankings.domain.model.team import TeamID


class TeamData(object):
    def __init__(self) -> None:
        self.wins = 0
        self.losses = 0


class TeamRecordService(object):
    def __init__(self, repository: TeamRecordRepository) -> None:
        self._repository = repository

    def calculate_for_season(
        self, season_ID: SeasonID, season_data: SeasonData
    ) -> List[TeamRecord]:
        team_data: Dict[TeamID, TeamData] = {}

        for game in season_data.game_map.values():
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
                        winning_data = TeamData()
                        team_data[game.winning_team_ID] = winning_data
                    winning_data.wins += 1

                if game.losing_team_ID is not None:
                    losing_data = team_data.get(game.losing_team_ID)
                    if losing_data is None:
                        losing_data = TeamData()
                        team_data[game.losing_team_ID] = losing_data
                    losing_data.losses += 1

        record_values = [
            TeamRecordValue(ID, data.wins, data.losses)
            for ID, data in team_data.items()
        ]

        return [self._repository.create(season_ID, None, record_values)]
