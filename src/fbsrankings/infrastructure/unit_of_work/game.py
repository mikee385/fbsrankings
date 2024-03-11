import datetime
from typing import List
from typing import Optional

from fbsrankings.common import Event
from fbsrankings.common import EventBus
from fbsrankings.domain import Game
from fbsrankings.domain import GameEventHandler as BaseEventHandler
from fbsrankings.domain import GameID
from fbsrankings.domain import GameRepository as BaseRepository
from fbsrankings.domain import SeasonID
from fbsrankings.domain import SeasonSection
from fbsrankings.domain import TeamID
from fbsrankings.event import GameCanceledEvent
from fbsrankings.event import GameCompletedEvent
from fbsrankings.event import GameCreatedEvent
from fbsrankings.event import GameNotesUpdatedEvent
from fbsrankings.event import GameRescheduledEvent
from fbsrankings.infrastructure.memory.write import (
    GameRepository as MemoryRepository,
)


class GameRepository(BaseRepository):
    def __init__(self, repository: BaseRepository, cache: MemoryRepository) -> None:
        super().__init__(repository._bus)
        self._cache = cache
        self._repository = repository

    def create(
        self,
        season_id: SeasonID,
        week: int,
        date: datetime.date,
        season_section: SeasonSection,
        home_team_id: TeamID,
        away_team_id: TeamID,
        notes: str,
    ) -> Game:
        return self._repository.create(
            season_id,
            week,
            date,
            season_section,
            home_team_id,
            away_team_id,
            notes,
        )

    def get(self, id_: GameID) -> Optional[Game]:
        game = self._cache.get(id_)
        if game is None:
            game = self._repository.get(id_)
        return game

    def find(
        self,
        season_id: SeasonID,
        week: int,
        team1_id: TeamID,
        team2_id: TeamID,
    ) -> Optional[Game]:
        game = self._cache.find(season_id, week, team1_id, team2_id)
        if game is None:
            game = self._repository.find(season_id, week, team1_id, team2_id)
        return game


class GameEventHandler(BaseEventHandler):
    def __init__(self, events: List[Event], bus: EventBus) -> None:
        super().__init__(bus)
        self._events = events

    def handle_created(self, event: GameCreatedEvent) -> None:
        self._events.append(event)

    def handle_rescheduled(self, event: GameRescheduledEvent) -> None:
        self._events.append(event)

    def handle_canceled(self, event: GameCanceledEvent) -> None:
        self._events.append(event)

    def handle_completed(self, event: GameCompletedEvent) -> None:
        self._events.append(event)

    def handle_notes_updated(self, event: GameNotesUpdatedEvent) -> None:
        self._events.append(event)
