import datetime
from abc import ABCMeta
from abc import abstractmethod
from collections.abc import Iterable
from collections.abc import Sequence
from typing import Callable
from typing import Generic
from typing import NewType
from typing import Optional
from typing import TypeVar
from uuid import UUID
from uuid import uuid4

from communication.bus import EventBus
from fbsrankings.messages.event import GameRankingCalculatedEvent
from fbsrankings.messages.event import RankingValue as EventValue
from fbsrankings.messages.event import TeamRankingCalculatedEvent
from fbsrankings.messages.query import AffiliationBySeasonResult
from fbsrankings.messages.query import GameBySeasonResult
from fbsrankings.ranking.command.domain.model.core import GameID
from fbsrankings.ranking.command.domain.model.core import SeasonID
from fbsrankings.ranking.command.domain.model.core import TeamID
from fbsrankings.typing_helpers import SupportsRichComparison


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
        self.game_map = {game.game_id: game for game in games}


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
        value_map: dict[T, float],
        sort_key: Callable[[SeasonData, T, float], SupportsRichComparison],
    ) -> list["RankingValue[T]"]:
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


class TeamRankingCalculator:  # noqa: PIE798
    @staticmethod
    def to_values(
        season_data: SeasonData,
        value_map: dict[TeamID, float],
    ) -> list[RankingValue[TeamID]]:
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
    ) -> tuple[float, str, str]:
        affiliation = season_data.affiliation_map[str(team_id)]
        return (-value, affiliation.team_name.upper(), str(team_id))


class TeamRankingFactory:
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
                event_id=str(uuid4()),
                ranking_id=str(ranking.id_),
                name=ranking.name,
                season_id=str(ranking.season_id),
                week=ranking.week,
                values=[
                    EventValue(
                        id=str(value.id_),
                        order=value.order,
                        rank=value.rank,
                        value=value.value,
                    )
                    for value in ranking.values
                ],
            ),
        )

        return ranking


class TeamRankingRepository(metaclass=ABCMeta):
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


class GameRankingCalculator:  # noqa: PIE798
    @staticmethod
    def to_values(
        season_data: SeasonData,
        value_map: dict[GameID, float],
    ) -> list[RankingValue[GameID]]:
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
    ) -> tuple[float, datetime.date, str, str, str]:
        game = season_data.game_map[str(game_id)]
        home_affiliation = season_data.affiliation_map[game.home_team_id]
        away_affiliation = season_data.affiliation_map[game.away_team_id]

        return (
            -value,
            game.date.ToDatetime().date(),
            home_affiliation.team_name.upper(),
            away_affiliation.team_name.upper(),
            str(game_id),
        )


class GameRankingFactory:
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
                event_id=str(uuid4()),
                ranking_id=str(ranking.id_),
                name=ranking.name,
                season_id=str(ranking.season_id),
                week=ranking.week,
                values=[
                    EventValue(
                        id=str(value.id_),
                        order=value.order,
                        rank=value.rank,
                        value=value.value,
                    )
                    for value in ranking.values
                ],
            ),
        )

        return ranking


class GameRankingRepository(metaclass=ABCMeta):
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
