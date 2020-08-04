from abc import ABCMeta
from abc import abstractmethod
from typing import Generic
from typing import Optional
from typing import TypeVar

from fbsrankings.common import Event
from fbsrankings.common import EventBus
from fbsrankings.common import Identifier
from fbsrankings.domain import GameID
from fbsrankings.domain import GameRankingRepository as BaseGameRankingRepository
from fbsrankings.domain import Ranking
from fbsrankings.domain import RankingID
from fbsrankings.domain import RankingValue
from fbsrankings.domain import SeasonID
from fbsrankings.domain import TeamID
from fbsrankings.domain import TeamRankingRepository as BaseTeamRankingRepository
from fbsrankings.event import GameRankingCalculatedEvent
from fbsrankings.event import RankingCalculatedEvent
from fbsrankings.event import TeamRankingCalculatedEvent
from fbsrankings.infrastructure.memory.storage import RankingDto
from fbsrankings.infrastructure.memory.storage import RankingStorage
from fbsrankings.infrastructure.memory.storage import RankingValueDto


T = TypeVar("T", bound=Identifier)


class RankingRepository(Generic[T], metaclass=ABCMeta):
    def __init__(self, storage: RankingStorage, bus: EventBus) -> None:
        self._bus = bus
        self._storage = storage

    def get(self, id: RankingID) -> Optional[Ranking[T]]:
        dto = self._storage.get(id.value)
        return self._to_ranking(dto) if dto is not None else None

    def find(
        self, name: str, season_id: SeasonID, week: Optional[int],
    ) -> Optional[Ranking[T]]:
        dto = self._storage.find(name, season_id.value, week)
        return self._to_ranking(dto) if dto is not None else None

    def _to_ranking(self, dto: RankingDto) -> Ranking[T]:
        return Ranking[T](
            self._bus,
            RankingID(dto.id),
            dto.name,
            SeasonID(dto.season_id),
            dto.week,
            [self._to_value(value) for value in dto.values],
        )

    @abstractmethod
    def _to_value(self, dto: RankingValueDto) -> RankingValue[T]:
        raise NotImplementedError

    @abstractmethod
    def handle(self, event: Event) -> bool:
        raise NotImplementedError

    def _handle_ranking_calculated(self, event: RankingCalculatedEvent) -> None:
        self._storage.add(
            RankingDto(
                event.id,
                event.name,
                event.season_id,
                event.week,
                [
                    RankingValueDto(value.id, value.order, value.rank, value.value)
                    for value in event.values
                ],
            ),
        )


class TeamRankingRepository(RankingRepository[TeamID], BaseTeamRankingRepository):
    def __init__(self, storage: RankingStorage, bus: EventBus) -> None:
        RankingRepository.__init__(self, storage, bus)
        BaseTeamRankingRepository.__init__(self, bus)

    def _to_value(self, dto: RankingValueDto) -> RankingValue[TeamID]:
        return RankingValue[TeamID](TeamID(dto.id), dto.order, dto.rank, dto.value)

    def handle(self, event: Event) -> bool:
        if isinstance(event, TeamRankingCalculatedEvent):
            self._handle_ranking_calculated(event)
            return True
        else:
            return False


class GameRankingRepository(RankingRepository[GameID], BaseGameRankingRepository):
    def __init__(self, storage: RankingStorage, bus: EventBus) -> None:
        RankingRepository.__init__(self, storage, bus)
        BaseGameRankingRepository.__init__(self, bus)

    def _to_value(self, dto: RankingValueDto) -> RankingValue[GameID]:
        return RankingValue[GameID](GameID(dto.id), dto.order, dto.rank, dto.value)

    def handle(self, event: Event) -> bool:
        if isinstance(event, GameRankingCalculatedEvent):
            self._handle_ranking_calculated(event)
            return True
        else:
            return False
