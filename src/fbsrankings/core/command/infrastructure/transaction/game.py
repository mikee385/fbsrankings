from typing import List
from typing import Optional

from fbsrankings.core.command.domain.model.game import Game
from fbsrankings.core.command.domain.model.game import GameID
from fbsrankings.core.command.domain.model.game import GameRepository as BaseRepository
from fbsrankings.core.command.domain.model.season import SeasonID
from fbsrankings.core.command.domain.model.team import TeamID
from fbsrankings.core.command.infrastructure.memory.game import (
    GameRepository as MemoryRepository,
)
from fbsrankings.shared.event import GameCanceledEvent
from fbsrankings.shared.event import GameCompletedEvent
from fbsrankings.shared.event import GameCreatedEvent
from fbsrankings.shared.event import GameEventHandler as BaseEventHandler
from fbsrankings.shared.event import GameNotesUpdatedEvent
from fbsrankings.shared.event import GameRescheduledEvent
from fbsrankings.shared.messaging import Event
from fbsrankings.shared.messaging import EventBus


class GameRepository(BaseRepository):
    def __init__(
        self,
        repository: BaseRepository,
        cache: MemoryRepository,
        cache_bus: EventBus,
    ) -> None:
        self._repository = repository
        self._cache = cache
        self._cache_bus = cache_bus

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
        cache_bus: EventBus,
    ) -> None:
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
