import datetime
from abc import ABCMeta
from abc import abstractmethod
from types import TracebackType
from typing import Callable
from typing import ContextManager
from typing import Dict
from typing import Generic
from typing import Iterable
from typing import List
from typing import NewType
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Type
from typing import TypeVar
from uuid import UUID
from uuid import uuid4

from typing_extensions import Literal

from fbsrankings.common import EventBus
from fbsrankings.common import SupportsRichComparison
from fbsrankings.core.query import AffiliationBySeasonResult
from fbsrankings.core.query import GameBySeasonResult
from fbsrankings.ranking.command.domain.model.core import GameID
from fbsrankings.ranking.command.domain.model.core import SeasonID
from fbsrankings.ranking.command.domain.model.core import TeamID
from fbsrankings.ranking.command.event.ranking import GameRankingCalculatedEvent
from fbsrankings.ranking.command.event.ranking import RankingValue as EventValue
from fbsrankings.ranking.command.event.ranking import TeamRankingCalculatedEvent


T = TypeVar("T", bound=UUID)


class SeasonData:
    def __init__(
        self,
        season_id: UUID,
        affiliations: Iterable[AffiliationBySeasonResult],
        games: Iterable[GameBySeasonResult],
    ) -> None:
        self.season_id = season_id
        self.affiliation_map = {
            affiliation.team_id: affiliation for affiliation in affiliations
        }
        self.game_map = {game.id_: game for game in games}


RankingID = NewType("RankingID", UUID)


class RankingValue(Generic[T]):
    def __init__(self, id_: T, order: int, rank: int, value: float) -> None:
        self._id = id_
        self._order = order
        self._rank = rank
        self._value = value

    @property
    def id_(self) -> T:
        return self._id

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
        sort_key: Callable[[SeasonData, T, float], SupportsRichComparison],
    ) -> List["RankingValue[T]"]:
        sorted_values = sorted(
            value_map.items(),
            key=lambda t: sort_key(season_data, t[0], t[1]),
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
        id_: RankingID,
        name: str,
        season_id: SeasonID,
        week: Optional[int],
        values: Iterable[RankingValue[T]],
    ) -> None:
        self._bus = bus
        self._id = id_
        self._name = name
        self._season_id = season_id
        self._week = week
        self._values = sorted(values, key=lambda v: v.order)

    @property
    def id_(self) -> RankingID:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def season_id(self) -> SeasonID:
        return self._season_id

    @property
    def week(self) -> Optional[int]:
        return self._week

    @property
    def values(self) -> Sequence[RankingValue[T]]:
        return self._values


class TeamRankingCalculator:
    @staticmethod
    def to_values(
        season_data: SeasonData,
        value_map: Dict[TeamID, float],
    ) -> List[RankingValue[TeamID]]:
        return RankingValue.to_values(
            season_data,
            value_map,
            TeamRankingCalculator.sort_key,
        )

    @staticmethod
    def sort_key(
        season_data: SeasonData,
        team_id: TeamID,
        value: float,
    ) -> Tuple[float, str, str]:
        affiliation = season_data.affiliation_map[team_id]
        return (-value, affiliation.team_name.upper(), str(team_id))


class TeamRankingRepository(metaclass=ABCMeta):
    def __init__(self, bus: EventBus) -> None:
        self._bus = bus

    def create(
        self,
        name: str,
        season_id: SeasonID,
        week: Optional[int],
        values: Iterable[RankingValue[TeamID]],
    ) -> Ranking[TeamID]:
        id_ = RankingID(uuid4())
        ranking = Ranking(self._bus, id_, name, season_id, week, values)
        self._bus.publish(
            TeamRankingCalculatedEvent(
                ranking.id_,
                ranking.name,
                ranking.season_id,
                ranking.week,
                [
                    EventValue(value.id_, value.order, value.rank, value.value)
                    for value in ranking.values
                ],
            ),
        )

        return ranking

    @abstractmethod
    def get(self, id_: RankingID) -> Optional[Ranking[TeamID]]:
        raise NotImplementedError

    @abstractmethod
    def find(
        self,
        name: str,
        season_id: SeasonID,
        week: Optional[int],
    ) -> Optional[Ranking[TeamID]]:
        raise NotImplementedError


class TeamRankingEventHandler(
    ContextManager["TeamRankingEventHandler"],
    metaclass=ABCMeta,
):
    def __init__(self, bus: EventBus) -> None:
        self._bus = bus

        self._bus.register_handler(TeamRankingCalculatedEvent, self.handle_calculated)

    def close(self) -> None:
        self._bus.unregister_handler(TeamRankingCalculatedEvent, self.handle_calculated)

    @abstractmethod
    def handle_calculated(self, event: TeamRankingCalculatedEvent) -> None:
        raise NotImplementedError

    def __enter__(self) -> "TeamRankingEventHandler":
        return self

    def __exit__(
        self,
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        return False


class GameRankingCalculator:
    @staticmethod
    def to_values(
        season_data: SeasonData,
        value_map: Dict[GameID, float],
    ) -> List[RankingValue[GameID]]:
        return RankingValue.to_values(
            season_data,
            value_map,
            GameRankingCalculator.sort_key,
        )

    @staticmethod
    def sort_key(
        season_data: SeasonData,
        game_id: GameID,
        value: float,
    ) -> Tuple[float, datetime.date, str, str, str]:
        game = season_data.game_map[game_id]
        home_affiliation = season_data.affiliation_map[game.home_team_id]
        away_affiliation = season_data.affiliation_map[game.away_team_id]

        return (
            -value,
            game.date,
            home_affiliation.team_name.upper(),
            away_affiliation.team_name.upper(),
            str(game_id),
        )


class GameRankingRepository(metaclass=ABCMeta):
    def __init__(self, bus: EventBus) -> None:
        self._bus = bus

    def create(
        self,
        name: str,
        season_id: SeasonID,
        week: Optional[int],
        values: Iterable[RankingValue[GameID]],
    ) -> Ranking[GameID]:
        id_ = RankingID(uuid4())
        ranking = Ranking(self._bus, id_, name, season_id, week, values)
        self._bus.publish(
            GameRankingCalculatedEvent(
                ranking.id_,
                ranking.name,
                ranking.season_id,
                ranking.week,
                [
                    EventValue(value.id_, value.order, value.rank, value.value)
                    for value in ranking.values
                ],
            ),
        )

        return ranking

    @abstractmethod
    def get(self, id_: RankingID) -> Optional[Ranking[GameID]]:
        raise NotImplementedError

    @abstractmethod
    def find(
        self,
        name: str,
        season_id: SeasonID,
        week: Optional[int],
    ) -> Optional[Ranking[GameID]]:
        raise NotImplementedError


class GameRankingEventHandler(
    ContextManager["GameRankingEventHandler"],
    metaclass=ABCMeta,
):
    def __init__(self, bus: EventBus) -> None:
        self._bus = bus

        self._bus.register_handler(GameRankingCalculatedEvent, self.handle_calculated)

    def close(self) -> None:
        self._bus.unregister_handler(GameRankingCalculatedEvent, self.handle_calculated)

    @abstractmethod
    def handle_calculated(self, event: GameRankingCalculatedEvent) -> None:
        raise NotImplementedError

    def __enter__(self) -> "GameRankingEventHandler":
        return self

    def __exit__(
        self,
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        return False
