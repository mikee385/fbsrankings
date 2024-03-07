from types import TracebackType
from typing import ContextManager
from typing import Optional
from typing import Type

from typing_extensions import Literal

from fbsrankings.common import EventBus
from fbsrankings.domain import SeasonID
from fbsrankings.domain import TeamID
from fbsrankings.domain import TeamRecord
from fbsrankings.domain import TeamRecordID
from fbsrankings.domain import TeamRecordRepository as BaseRepository
from fbsrankings.domain import TeamRecordValue
from fbsrankings.event import TeamRecordCalculatedEvent
from fbsrankings.infrastructure.memory.storage import TeamRecordDto
from fbsrankings.infrastructure.memory.storage import TeamRecordStorage
from fbsrankings.infrastructure.memory.storage import TeamRecordValueDto


class TeamRecordRepository(BaseRepository, ContextManager["TeamRecordRepository"]):
    def __init__(self, storage: TeamRecordStorage, bus: EventBus) -> None:
        super().__init__(bus)
        self._storage = storage

        self._bus.register_handler(
            TeamRecordCalculatedEvent,
            self._handle_record_calculated,
        )

    def close(self) -> None:
        self._bus.unregister_handler(
            TeamRecordCalculatedEvent,
            self._handle_record_calculated,
        )

    def get(self, id_: TeamRecordID) -> Optional[TeamRecord]:
        dto = self._storage.get(id_.value)
        return self._to_record(dto) if dto is not None else None

    def find(self, season_id: SeasonID, week: Optional[int]) -> Optional[TeamRecord]:
        dto = self._storage.find(season_id.value, week)
        return self._to_record(dto) if dto is not None else None

    def _to_record(self, dto: TeamRecordDto) -> TeamRecord:
        return TeamRecord(
            self._bus,
            TeamRecordID(dto.id_),
            SeasonID(dto.season_id),
            dto.week,
            [self._to_value(value) for value in dto.values],
        )

    @staticmethod
    def _to_value(dto: TeamRecordValueDto) -> TeamRecordValue:
        return TeamRecordValue(TeamID(dto.team_id), dto.wins, dto.losses)

    def _handle_record_calculated(self, event: TeamRecordCalculatedEvent) -> None:
        self._storage.add(
            TeamRecordDto(
                event.id_,
                event.season_id,
                event.week,
                [
                    TeamRecordValueDto(value.team_id, value.wins, value.losses)
                    for value in event.values
                ],
            ),
        )

    def __enter__(self) -> "TeamRecordRepository":
        return self

    def __exit__(
        self,
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        return False
