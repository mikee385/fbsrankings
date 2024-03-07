from types import TracebackType
from typing import Callable
from typing import ContextManager
from typing import Generic
from typing import Optional
from typing import Type
from typing import TypeVar

from typing_extensions import Literal

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


class RankingRepository(Generic[T]):
    def __init__(
        self,
        storage: RankingStorage,
        bus: EventBus,
        to_value: Callable[[RankingValueDto], RankingValue[T]],
    ) -> None:
        self._bus = bus
        self._storage = storage
        self._to_value = to_value

    def get(self, id_: RankingID) -> Optional[Ranking[T]]:
        dto = self._storage.get(id_.value)
        return self._to_ranking(dto) if dto is not None else None

    def find(
        self,
        name: str,
        season_id: SeasonID,
        week: Optional[int],
    ) -> Optional[Ranking[T]]:
        dto = self._storage.find(name, season_id.value, week)
        return self._to_ranking(dto) if dto is not None else None

    def _to_ranking(self, dto: RankingDto) -> Ranking[T]:
        return Ranking[T](
            self._bus,
            RankingID(dto.id_),
            dto.name,
            SeasonID(dto.season_id),
            dto.week,
            [self._to_value(value) for value in dto.values],
        )

    def handle_ranking_calculated(self, event: RankingCalculatedEvent) -> None:
        self._storage.add(
            RankingDto(
                event.id_,
                event.name,
                event.season_id,
                event.week,
                [
                    RankingValueDto(value.id_, value.order, value.rank, value.value)
                    for value in event.values
                ],
            ),
        )


class TeamRankingRepository(
    BaseTeamRankingRepository,
    ContextManager["TeamRankingRepository"],
):
    def __init__(self, storage: RankingStorage, bus: EventBus) -> None:
        super().__init__(bus)
        self._repository = RankingRepository[TeamID](storage, bus, self._to_value)

        self._bus.register_handler(
            TeamRankingCalculatedEvent,
            self._repository.handle_ranking_calculated,
        )

    def close(self) -> None:
        self._bus.unregister_handler(
            TeamRankingCalculatedEvent,
            self._repository.handle_ranking_calculated,
        )

    def get(self, id_: RankingID) -> Optional[Ranking[TeamID]]:
        return self._repository.get(id_)

    def find(
        self,
        name: str,
        season_id: SeasonID,
        week: Optional[int],
    ) -> Optional[Ranking[TeamID]]:
        return self._repository.find(name, season_id, week)

    @staticmethod
    def _to_value(dto: RankingValueDto) -> RankingValue[TeamID]:
        return RankingValue[TeamID](TeamID(dto.id_), dto.order, dto.rank, dto.value)

    def __enter__(self) -> "TeamRankingRepository":
        return self

    def __exit__(
        self,
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        return False


class GameRankingRepository(
    BaseGameRankingRepository,
    ContextManager["GameRankingRepository"],
):
    def __init__(self, storage: RankingStorage, bus: EventBus) -> None:
        super().__init__(bus)
        self._repository = RankingRepository[GameID](storage, bus, self._to_value)

        self._bus.register_handler(
            GameRankingCalculatedEvent,
            self._repository.handle_ranking_calculated,
        )

    def close(self) -> None:
        self._bus.unregister_handler(
            GameRankingCalculatedEvent,
            self._repository.handle_ranking_calculated,
        )

    def get(self, id_: RankingID) -> Optional[Ranking[GameID]]:
        return self._repository.get(id_)

    def find(
        self,
        name: str,
        season_id: SeasonID,
        week: Optional[int],
    ) -> Optional[Ranking[GameID]]:
        return self._repository.find(name, season_id, week)

    @staticmethod
    def _to_value(dto: RankingValueDto) -> RankingValue[GameID]:
        return RankingValue[GameID](GameID(dto.id_), dto.order, dto.rank, dto.value)

    def __enter__(self) -> "GameRankingRepository":
        return self

    def __exit__(
        self,
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        return False
