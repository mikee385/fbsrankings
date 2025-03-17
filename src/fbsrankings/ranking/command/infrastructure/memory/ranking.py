from collections.abc import Sequence
from typing import Callable
from typing import Generic
from typing import Optional
from typing import TypeVar
from uuid import UUID

from communication.bus import EventBus
from fbsrankings.messages.event import GameRankingCalculatedEvent
from fbsrankings.messages.event import RankingValue as EventValue
from fbsrankings.messages.event import TeamRankingCalculatedEvent
from fbsrankings.ranking.command.domain.model.core import GameID
from fbsrankings.ranking.command.domain.model.core import SeasonID
from fbsrankings.ranking.command.domain.model.core import TeamID
from fbsrankings.ranking.command.domain.model.ranking import (
    GameRankingRepository as BaseGameRankingRepository,
)
from fbsrankings.ranking.command.domain.model.ranking import Ranking
from fbsrankings.ranking.command.domain.model.ranking import RankingID
from fbsrankings.ranking.command.domain.model.ranking import RankingValue
from fbsrankings.ranking.command.domain.model.ranking import (
    TeamRankingRepository as BaseTeamRankingRepository,
)
from fbsrankings.ranking.command.infrastructure.shared.ranking import (
    GameRankingEventHandler as BaseGameRankingEventHandler,
)
from fbsrankings.ranking.command.infrastructure.shared.ranking import (
    TeamRankingEventHandler as BaseTeamRankingEventHandler,
)
from fbsrankings.storage.memory import RankingDto
from fbsrankings.storage.memory import RankingStorage
from fbsrankings.storage.memory import RankingValueDto


T = TypeVar("T", bound=UUID)


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
        dto = self._storage.get(str(id_))
        return self._to_ranking(dto) if dto is not None else None

    def find(
        self,
        name: str,
        season_id: SeasonID,
        week: Optional[int],
    ) -> Optional[Ranking[T]]:
        dto = self._storage.find(name, str(season_id), week)
        return self._to_ranking(dto) if dto is not None else None

    def _to_ranking(self, dto: RankingDto) -> Ranking[T]:
        return Ranking[T](
            self._bus,
            RankingID(UUID(dto.id_)),
            dto.name,
            SeasonID(UUID(dto.season_id)),
            dto.week,
            [self._to_value(value) for value in dto.values],
        )


class RankingEventHandler:
    def __init__(self, storage: RankingStorage) -> None:
        self._storage = storage

    def handle_calculated(
        self,
        ranking_id: str,
        name: str,
        season_id: str,
        week: Optional[int],
        values: Sequence[EventValue],
    ) -> None:
        self._storage.add(
            RankingDto(
                ranking_id,
                name,
                season_id,
                week,
                [
                    RankingValueDto(
                        value.id,
                        value.order,
                        value.rank,
                        value.value,
                    )
                    for value in values
                ],
            ),
        )


class TeamRankingRepository(BaseTeamRankingRepository):
    def __init__(self, storage: RankingStorage, bus: EventBus) -> None:
        self._repository = RankingRepository[TeamID](storage, bus, self._to_value)

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
        return RankingValue[TeamID](
            TeamID(UUID(dto.id_)),
            dto.order,
            dto.rank,
            dto.value,
        )


class TeamRankingEventHandler(BaseTeamRankingEventHandler):
    def __init__(self, storage: RankingStorage) -> None:
        self._event_handler = RankingEventHandler(storage)

    def handle_calculated(
        self,
        event: TeamRankingCalculatedEvent,
    ) -> None:
        self._event_handler.handle_calculated(
            event.ranking_id,
            event.name,
            event.season_id,
            event.week if event.HasField("week") else None,
            event.values,
        )


class GameRankingRepository(BaseGameRankingRepository):
    def __init__(self, storage: RankingStorage, bus: EventBus) -> None:
        self._repository = RankingRepository[GameID](storage, bus, self._to_value)

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
        return RankingValue[GameID](
            GameID(UUID(dto.id_)),
            dto.order,
            dto.rank,
            dto.value,
        )


class GameRankingEventHandler(BaseGameRankingEventHandler):
    def __init__(self, storage: RankingStorage) -> None:
        self._event_handler = RankingEventHandler(storage)

    def handle_calculated(
        self,
        event: GameRankingCalculatedEvent,
    ) -> None:
        self._event_handler.handle_calculated(
            event.ranking_id,
            event.name,
            event.season_id,
            event.week if event.HasField("week") else None,
            event.values,
        )
