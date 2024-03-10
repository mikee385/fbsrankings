import datetime
from typing import Optional

from fbsrankings.domain import Game
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
from fbsrankings.infrastructure.memory.storage import (
    GameStorage as MemoryStorage,
)
from fbsrankings.infrastructure.memory.write import (
    GameRepository as MemoryRepository,
)


class GameRepository(BaseRepository):
    def __init__(self, repository: BaseRepository) -> None:
        super().__init__(repository._bus)
        self._cache = MemoryRepository(MemoryStorage(), self._bus)
        self._repository = repository

        self._bus.register_handler(GameCreatedEvent, self._cache.handle_created)
        self._bus.register_handler(GameRescheduledEvent, self._cache.handle_rescheduled)
        self._bus.register_handler(GameCanceledEvent, self._cache.handle_canceled)
        self._bus.register_handler(GameCompletedEvent, self._cache.handle_completed)
        self._bus.register_handler(
            GameNotesUpdatedEvent,
            self._cache.handle_notes_updated,
        )

    def close(self) -> None:
        self._bus.unregister_handler(GameCreatedEvent, self._cache.handle_created)
        self._bus.unregister_handler(
            GameRescheduledEvent,
            self._cache.handle_rescheduled,
        )
        self._bus.unregister_handler(GameCanceledEvent, self._cache.handle_canceled)
        self._bus.unregister_handler(GameCompletedEvent, self._cache.handle_completed)
        self._bus.unregister_handler(
            GameNotesUpdatedEvent,
            self._cache.handle_notes_updated,
        )

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
