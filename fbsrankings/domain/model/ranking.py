from abc import ABCMeta
from abc import abstractmethod
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
from fbsrankings.event import RankingCreatedEvent
from fbsrankings.event import RankingValue as EventValue
from fbsrankings.event import RankingValuesUpdatedEvent


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
        self.games = [games]


class RankingID(Identifier):
    pass


class RankingValue(Generic[T]):
    def __init__(self, ID: T, rank: int, order: int, value: float) -> None:
        self._ID = ID
        self._rank = rank
        self._order = order
        self._value = value

    @property
    def ID(self) -> T:
        return self._ID

    @property
    def rank(self) -> int:
        return self._rank

    @property
    def order(self) -> int:
        return self._order

    @property
    def value(self) -> float:
        return self._value


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

    @values.setter
    def values(self, values: Iterable[RankingValue[T]]) -> None:
        if not values:
            raise ValueError("values must not be empty")
        self._values = sorted(values, key=lambda v: v.order)
        self._bus.publish(RankingValuesUpdatedEvent(self.ID.value, self._event_values))

    @property
    def _event_values(self) -> List[EventValue]:
        return list(
            map(lambda v: EventValue(v.ID.value, v.rank, v.order, v.value), self.values)
        )


class RankingService(Generic[T], metaclass=ABCMeta):
    def __init__(self, bus: EventBus) -> None:
        self._bus = bus

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
        season_ID: SeasonID,
        week: Optional[int],
        values: Iterable[RankingValue[T]],
    ) -> Ranking[T]:
        ID = RankingID(uuid4())
        ranking = Ranking(self._bus, ID, name, season_ID, week, values)
        self._bus.publish(
            RankingCreatedEvent(
                ranking.ID.value,
                ranking.name,
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
