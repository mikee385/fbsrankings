from typing import Optional
from uuid import UUID

from communication.bus import EventBus
from fbsrankings.messages.event import TeamRecordCalculatedEvent
from fbsrankings.messages.event import TeamRecordEventHandler as BaseEventHandler
from fbsrankings.ranking.command.domain.model.core import SeasonID
from fbsrankings.ranking.command.domain.model.core import TeamID
from fbsrankings.ranking.command.domain.model.record import TeamRecord
from fbsrankings.ranking.command.domain.model.record import TeamRecordID
from fbsrankings.ranking.command.domain.model.record import (
    TeamRecordRepository as BaseRepository,
)
from fbsrankings.ranking.command.domain.model.record import TeamRecordValue
from fbsrankings.storage.memory import TeamRecordDto
from fbsrankings.storage.memory import TeamRecordStorage
from fbsrankings.storage.memory import TeamRecordValueDto


class TeamRecordRepository(BaseRepository):
    def __init__(self, storage: TeamRecordStorage, bus: EventBus) -> None:
        self._storage = storage
        self._bus = bus

    def get(self, id_: TeamRecordID) -> Optional[TeamRecord]:
        dto = self._storage.get(str(id_))
        return self._to_record(dto) if dto is not None else None

    def find(self, season_id: SeasonID, week: Optional[int]) -> Optional[TeamRecord]:
        dto = self._storage.find(str(season_id), week)
        return self._to_record(dto) if dto is not None else None

    def _to_record(self, dto: TeamRecordDto) -> TeamRecord:
        return TeamRecord(
            self._bus,
            TeamRecordID(UUID(dto.id_)),
            SeasonID(UUID(dto.season_id)),
            dto.week,
            [self._to_value(value) for value in dto.values],
        )

    @staticmethod
    def _to_value(dto: TeamRecordValueDto) -> TeamRecordValue:
        return TeamRecordValue(TeamID(UUID(dto.team_id)), dto.wins, dto.losses)


class TeamRecordEventHandler(BaseEventHandler):
    def __init__(self, storage: TeamRecordStorage) -> None:
        self._storage = storage

    def handle_calculated(self, event: TeamRecordCalculatedEvent) -> None:
        self._storage.add(
            TeamRecordDto(
                event.record_id,
                event.season_id,
                event.week,
                [
                    TeamRecordValueDto(value.team_id, value.wins, value.losses)
                    for value in event.values
                ],
            ),
        )
