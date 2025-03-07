from typing import List
from typing import Optional
from uuid import uuid4

from communication.bus import EventBus
from communication.messages import Event
from fbsrankings.messages.event import TeamRecordCalculatedEvent
from fbsrankings.messages.event import TeamRecordEventHandler as BaseEventHandler
from fbsrankings.messages.event import TeamRecordValue as EventValue
from fbsrankings.ranking.command.domain.model.core import SeasonID
from fbsrankings.ranking.command.domain.model.record import TeamRecord
from fbsrankings.ranking.command.domain.model.record import TeamRecordID
from fbsrankings.ranking.command.domain.model.record import (
    TeamRecordRepository as BaseRepository,
)
from fbsrankings.ranking.command.infrastructure.memory.record import (
    TeamRecordRepository as MemoryRepository,
)


class TeamRecordRepository(BaseRepository):
    def __init__(
        self,
        repository: BaseRepository,
        cache: MemoryRepository,
        cache_bus: EventBus,
    ) -> None:
        self._repository = repository
        self._cache = cache
        self._cache_bus = cache_bus

    def get(self, id_: TeamRecordID) -> Optional[TeamRecord]:
        team_record = self._cache.get(id_)
        if team_record is None:
            team_record = self._repository.get(id_)
            if team_record is not None:
                self._cache_bus.publish(_created_event(team_record))
        return team_record

    def find(self, season_id: SeasonID, week: Optional[int]) -> Optional[TeamRecord]:
        team_record = self._cache.find(season_id, week)
        if team_record is None:
            team_record = self._repository.find(season_id, week)
            if team_record is not None:
                self._cache_bus.publish(_created_event(team_record))
        return team_record


def _created_event(record: TeamRecord) -> TeamRecordCalculatedEvent:
    return TeamRecordCalculatedEvent(
        uuid4(),
        record.id_,
        record.season_id,
        record.week,
        [
            EventValue(
                value.team_id,
                value.wins,
                value.losses,
                value.games,
                value.win_percentage,
            )
            for value in record.values
        ],
    )


class TeamRecordEventHandler(BaseEventHandler):
    def __init__(
        self,
        events: List[Event],
        cache_bus: EventBus,
    ) -> None:
        self._events = events
        self._cache_bus = cache_bus

    def handle_calculated(self, event: TeamRecordCalculatedEvent) -> None:
        self._events.append(event)
        self._cache_bus.publish(event)
