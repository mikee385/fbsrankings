import datetime
from abc import ABCMeta
from abc import abstractmethod
from typing import Any
from typing import Callable
from typing import Dict
from typing import Generic
from typing import Iterable
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import TypeVar
from uuid import uuid4

from fbsrankings.common import EventBus
from fbsrankings.common import Identifier
from fbsrankings.domain.model.affiliation import Affiliation
from fbsrankings.domain.model.game import Game
from fbsrankings.domain.model.game import GameID
from fbsrankings.domain.model.season import Season
from fbsrankings.domain.model.season import SeasonID
from fbsrankings.domain.model.team import Team
from fbsrankings.domain.model.team import TeamID
from fbsrankings.event import GameRankingCalculatedEvent
from fbsrankings.event import RankingValue as EventValue
from fbsrankings.event import TeamRankingCalculatedEvent


T = TypeVar("T", bound=Identifier)


class SeasonData(object):
    def __init__(
        self,
        season: Season,
        teams: Iterable[Team],
        affiliations: Iterable[Affiliation],
        games: Iterable[Game],
    ) -> None:
        self.season = season
        self.team_map = {team.ID: team for team in teams}
        self.affiliation_map = {
            affiliation.team_ID: affiliation for affiliation in affiliations
        }
        self.game_map = {game.ID: game for game in games}


class RankingID(Identifier):
    pass


class RankingValue(Generic[T]):
    def __init__(self, ID: T, order: int, rank: int, value: float) -> None:
        self._ID = ID
        self._order = order
        self._rank = rank
        self._value = value

    @property
    def ID(self) -> T:
        return self._ID

    @property
    def order(self) -> int:
        return self._order

    @property
    def rank(self) -> int:
        return self._rank

    @property
    def value(self) -> float:
        return self._value

    @staticmethod
    def to_values(
        season_data: SeasonData,
        value_map: Dict[T, float],
        sort_key: Callable[[SeasonData, T, float], Any],
    ) -> List["RankingValue[T]"]:
        sorted_values = sorted(
            value_map.items(), key=lambda t: sort_key(season_data, t[0], t[1])
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


class Ranking(Generic[T]):
    def __init__(
        self,
        bus: EventBus,
        ID: RankingID,
        name: str,
        season_ID: SeasonID,
        week: Optional[int],
        values: Iterable[RankingValue[T]],
    ) -> None:
        self._bus = bus
        self._ID = ID
        self._name = name
        self._season_ID = season_ID
        self._week = week
        self._values = sorted(values, key=lambda v: v.order)

    @property
    def ID(self) -> RankingID:
        return self._ID

    @property
    def name(self) -> str:
        return self._name

    @property
    def season_ID(self) -> SeasonID:
        return self._season_ID

    @property
    def week(self) -> Optional[int]:
        return self._week

    @property
    def values(self) -> Sequence[RankingValue[T]]:
        return self._values


class TeamRankingService(metaclass=ABCMeta):
    @staticmethod
    def _to_values(
        season_data: SeasonData, value_map: Dict[TeamID, float]
    ) -> List[RankingValue[TeamID]]:
        return RankingValue.to_values(
            season_data, value_map, TeamRankingService._sort_key
        )

    @staticmethod
    def _sort_key(
        season_data: SeasonData, team_ID: TeamID, value: float
    ) -> Tuple[float, str, str]:
        team = season_data.team_map[team_ID]
        return (-value, team.name.upper(), str(team_ID.value))


class TeamRankingRepository(metaclass=ABCMeta):
    def __init__(self, bus: EventBus) -> None:
        self._bus = bus

    def create(
        self,
        name: str,
        season_ID: SeasonID,
        week: Optional[int],
        values: Iterable[RankingValue[TeamID]],
    ) -> Ranking[TeamID]:
        ID = RankingID(uuid4())
        ranking = Ranking(self._bus, ID, name, season_ID, week, values)
        self._bus.publish(
            TeamRankingCalculatedEvent(
                ranking.ID.value,
                ranking.name,
                ranking.season_ID.value,
                ranking.week,
                [
                    EventValue(value.ID.value, value.order, value.rank, value.value)
                    for value in ranking.values
                ],
            )
        )

        return ranking

    @abstractmethod
    def get(self, ID: RankingID) -> Optional[Ranking[TeamID]]:
        raise NotImplementedError

    @abstractmethod
    def find(
        self, name: str, season_ID: SeasonID, week: Optional[int]
    ) -> Optional[Ranking[TeamID]]:
        raise NotImplementedError


class GameRankingService(metaclass=ABCMeta):
    @staticmethod
    def _to_values(
        season_data: SeasonData, value_map: Dict[GameID, float]
    ) -> List[RankingValue[GameID]]:
        return RankingValue.to_values(
            season_data, value_map, GameRankingService._sort_key
        )

    @staticmethod
    def _sort_key(
        season_data: SeasonData, game_ID: GameID, value: float
    ) -> Tuple[float, datetime.date, str, str, str]:
        game = season_data.game_map[game_ID]
        home_team = season_data.team_map[game.home_team_ID]
        away_team = season_data.team_map[game.away_team_ID]

        return (
            -value,
            game.date,
            home_team.name.upper(),
            away_team.name.upper(),
            str(game_ID.value),
        )


class GameRankingRepository(metaclass=ABCMeta):
    def __init__(self, bus: EventBus) -> None:
        self._bus = bus

    def create(
        self,
        name: str,
        season_ID: SeasonID,
        week: Optional[int],
        values: Iterable[RankingValue[GameID]],
    ) -> Ranking[GameID]:
        ID = RankingID(uuid4())
        ranking = Ranking(self._bus, ID, name, season_ID, week, values)
        self._bus.publish(
            GameRankingCalculatedEvent(
                ranking.ID.value,
                ranking.name,
                ranking.season_ID.value,
                ranking.week,
                [
                    EventValue(value.ID.value, value.order, value.rank, value.value)
                    for value in ranking.values
                ],
            )
        )

        return ranking

    @abstractmethod
    def get(self, ID: RankingID) -> Optional[Ranking[GameID]]:
        raise NotImplementedError

    @abstractmethod
    def find(
        self, name: str, season_ID: SeasonID, week: Optional[int]
    ) -> Optional[Ranking[GameID]]:
        raise NotImplementedError
