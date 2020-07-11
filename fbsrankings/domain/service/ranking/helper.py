from abc import ABCMeta
from abc import abstractmethod
from typing import Any
from typing import Dict
from typing import Generic
from typing import List
from typing import Tuple
from typing import TypeVar

from fbsrankings.common import Identifier
from fbsrankings.domain.model.ranking import RankingValue
from fbsrankings.domain.model.ranking import SeasonData
from fbsrankings.domain.model.team import TeamID


T = TypeVar("T", bound=Identifier)


class ValueHelper(Generic[T], metaclass=ABCMeta):
    def __init__(self, season_data: SeasonData) -> None:
        self._season_data = season_data

    @abstractmethod
    def _sort_key(self, ID: T, value: float) -> Any:
        raise NotImplementedError

    def to_values(self, value_map: Dict[T, float]) -> List[RankingValue[T]]:
        sorted_values = sorted(
            value_map.items(), key=lambda t: self._sort_key(t[0], t[1])
        )

        ranking_values = []
        previous_value = 0.0
        previous_rank = 0
        for order, item in enumerate(sorted_values):
            if item[1] == previous_value:
                rank = previous_rank
            else:
                rank = order

            previous_value = item[1]
            previous_rank = rank
            ranking_values.append(RankingValue(item[0], order + 1, rank + 1, item[1]))

        return ranking_values


class TeamValueHelper(ValueHelper[TeamID]):
    def __init__(self, season_data: SeasonData) -> None:
        super().__init__(season_data)

    def _sort_key(self, team_ID: TeamID, value: float) -> Tuple[float, str, str]:
        team = self._season_data.team_map.get(team_ID)
        if team is None:
            raise ValueError(f"Team not found for {team_ID}")
        return (-value, team.name.upper(), str(team_ID.value))
