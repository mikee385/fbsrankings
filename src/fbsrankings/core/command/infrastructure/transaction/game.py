import datetime
from typing import List
from typing import Optional

from fbsrankings.common import Event
from fbsrankings.common import EventBus
from fbsrankings.core.command.domain.model.game import Game
from fbsrankings.core.command.domain.model.game import (
    GameEventHandler as BaseEventHandler,
)
from fbsrankings.core.command.domain.model.game import GameID
from fbsrankings.core.command.domain.model.game import GameRepository as BaseRepository
from fbsrankings.core.command.domain.model.season import SeasonID
from fbsrankings.core.command.domain.model.team import TeamID
from fbsrankings.core.command.event.game import GameCanceledEvent
from fbsrankings.core.command.event.game import GameCompletedEvent
from fbsrankings.core.command.event.game import GameCreatedEvent
from fbsrankings.core.command.event.game import GameNotesUpdatedEvent
from fbsrankings.core.command.event.game import GameRescheduledEvent
from fbsrankings.core.command.infrastructure.memory.game import (
    GameRepository as MemoryRepository,
)
from fbsrankings.enum import SeasonSection


class GameRepository(BaseRepository):
    def __init__(
        self,
        repository: BaseRepository,
        cache: MemoryRepository,
        cache_bus: EventBus,
    ) -> None:
        super().__init__(repository._bus)
        self._repository = repository
        self._cache = cache
        self._cache_bus = cache_bus

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
            if game is not None:
                self._cache_bus.publish(_created_event(game))
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
            if game is not None:
                self._cache_bus.publish(_created_event(game))
        return game


def _created_event(game: Game) -> GameCreatedEvent:
    return GameCreatedEvent(
        game.id_,
        game.season_id,
        game.week,
        game.date,
        game.season_section.name,
        game.home_team_id,
        game.away_team_id,
        game.notes,
    )


class GameEventHandler(BaseEventHandler):
    def __init__(
        self,
        events: List[Event],
        event_bus: EventBus,
        cache_bus: EventBus,
    ) -> None:
        super().__init__(event_bus)
        self._events = events
        self._cache_bus = cache_bus

    def handle_created(self, event: GameCreatedEvent) -> None:
        self._events.append(event)
        self._cache_bus.publish(event)

    def handle_rescheduled(self, event: GameRescheduledEvent) -> None:
        self._events.append(event)
        self._cache_bus.publish(event)

    def handle_canceled(self, event: GameCanceledEvent) -> None:
        self._events.append(event)
        self._cache_bus.publish(event)

    def handle_completed(self, event: GameCompletedEvent) -> None:
        self._events.append(event)
        self._cache_bus.publish(event)

    def handle_notes_updated(self, event: GameNotesUpdatedEvent) -> None:
        self._events.append(event)
        self._cache_bus.publish(event)
