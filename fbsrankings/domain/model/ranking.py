from abc import ABCMeta
from abc import abstractmethod
from enum import Enum
from typing import Generic
from typing import Iterable
from typing import List
from typing import Optional
from typing import Sequence
from typing import TypeVar
from uuid import uuid4

from fbsrankings.common import EventBus
from fbsrankings.common import Identifier
from fbsrankings.domain.model.affiliation import Affiliation
from fbsrankings.domain.model.game import Game
from fbsrankings.domain.model.season import Season
from fbsrankings.domain.model.season import SeasonID
from fbsrankings.domain.model.team import Team
from fbsrankings.event import RankingCalculatedEvent
from fbsrankings.event import RankingValue as EventValue


T = TypeVar("T", bound=Identifier)


class SeasonData(object):
    def __init__(
        self,
        season: Season,
        teams: Iterable[Team],
        affiliations: Iterable[Affiliation],
        games: Iterable[Game],
    ):
        self.season = season
        self.team_map = {team.ID: team for team in teams}
        self.affiliation_map = {
            affiliation.team_ID: affiliation for affiliation in affiliations
        }
        self.games = [game for game in games]
        

class RankingType(Enum):
    TEAM = 0
    GAME = 1


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


class Ranking(Generic[T]):
    def __init__(
        self,
        bus: EventBus,
        ID: RankingID,
        name: str,
        type: RankingType,
        season_ID: SeasonID,
        week: Optional[int],
        values: Iterable[RankingValue[T]],
    ) -> None:
        self._bus = bus
        self._ID = ID
        self._name = name
        self._type = type
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
    def type(self) -> RankingType:
        return self._type

    @property
    def season_ID(self) -> SeasonID:
        return self._season_ID

    @property
    def week(self) -> Optional[int]:
        return self._week

    @property
    def values(self) -> Sequence[RankingValue[T]]:
        return self._values

    @property
    def _event_values(self) -> List[EventValue]:
        return list(
            map(lambda v: EventValue(v.ID.value, v.rank, v.order, v.value), self.values)
        )


class RankingService(Generic[T], metaclass=ABCMeta):
    @abstractmethod
    def calculate_for_season(
        self, season_ID: SeasonID, season_data: SeasonData
    ) -> List[Ranking[T]]:
        raise NotImplementedError


class RankingRepository(metaclass=ABCMeta):
    def __init__(self, bus: EventBus) -> None:
        self._bus = bus

    def create(
        self,
        name: str,
        type: RankingType,
        season_ID: SeasonID,
        week: Optional[int],
        values: Iterable[RankingValue[T]],
    ) -> Ranking[T]:
        ID = RankingID(uuid4())
        ranking = Ranking(self._bus, ID, name, type, season_ID, week, values)
        self._bus.publish(
            RankingCalculatedEvent(
                ranking.ID.value,
                ranking.name,
                ranking.type.name,
                ranking.season_ID.value,
                ranking.week,
                ranking._event_values,
            )
        )

        return ranking

    @abstractmethod
    def get(self, ID: RankingID) -> Optional[Ranking[T]]:
        raise NotImplementedError

    @abstractmethod
    def find(
        self, name: str, season_ID: SeasonID, week: Optional[int]
    ) -> Optional[Ranking[T]]:
        raise NotImplementedError
