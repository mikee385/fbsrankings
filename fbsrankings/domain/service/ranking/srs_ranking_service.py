from typing import Dict
from typing import List
from uuid import uuid4

from fbsrankings.domain.model.affiliation import Subdivision
from fbsrankings.domain.model.ranking import Ranking
from fbsrankings.domain.model.ranking import RankingID
from fbsrankings.domain.model.ranking import RankingService
from fbsrankings.domain.model.ranking import SeasonData
from fbsrankings.domain.model.season import SeasonID
from fbsrankings.domain.model.team import TeamID
from fbsrankings.domain.service.ranking.helper import TeamValueHelper


class SRSRankingService(RankingService[TeamID]):
    name: str = "SRS"

    def calculate_for_season(
        self, season_ID: SeasonID, season_data: SeasonData
    ) -> List[Ranking[TeamID]]:
        values: Dict[TeamID, float] = {}
        for _, affiliation in season_data.affiliation_map.items():
            if affiliation.subdivision == Subdivision.FBS:
                team = season_data.team_map[affiliation.team_ID]
                values[team.ID] = ord(team.name[0])

        helper = TeamValueHelper(season_data)
        ranking_values = helper.to_values(values)

        ID = RankingID(uuid4())
        return [
            Ranking(
                self._bus, ID, SRSRankingService.name, season_ID, None, ranking_values
            )
        ]
