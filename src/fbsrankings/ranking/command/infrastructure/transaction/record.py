from typing import Optional
from uuid import uuid4

from communication.bus import EventBus
from communication.messages import Event
from fbsrankings.messages.event import TeamRecordCalculatedEvent
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
from fbsrankings.ranking.command.infrastructure.shared.record import (
    TeamRecordEventHandler as BaseEventHandler,
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
        event_id=str(uuid4()),
        record_id=str(record.id_),
        season_id=str(record.season_id),
        week=record.week,
        values=[
            EventValue(
                team_id=str(value.team_id),
                wins=value.wins,
                losses=value.losses,
                games=value.games,
                win_percentage=value.win_percentage,
            )
            for value in record.values
        ],
    )


class TeamRecordEventHandler(BaseEventHandler):
    def __init__(
        self,
        events: list[Event],
        cache_bus: EventBus,
    ) -> None:
        self._events = events
        self._cache_bus = cache_bus

    def handle_calculated(self, event: TeamRecordCalculatedEvent) -> None:
        self._events.append(event)
        self._cache_bus.publish(event)
