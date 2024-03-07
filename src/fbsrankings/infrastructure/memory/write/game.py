from types import TracebackType
from typing import ContextManager
from typing import List
from typing import Optional
from typing import Type

from typing_extensions import Literal

from fbsrankings.common import EventBus
from fbsrankings.domain import Game
from fbsrankings.domain import GameID
from fbsrankings.domain import GameRepository as BaseRepository
from fbsrankings.domain import GameStatus
from fbsrankings.domain import SeasonID
from fbsrankings.domain import SeasonSection
from fbsrankings.domain import TeamID
from fbsrankings.event import GameCanceledEvent
from fbsrankings.event import GameCompletedEvent
from fbsrankings.event import GameCreatedEvent
from fbsrankings.event import GameNotesUpdatedEvent
from fbsrankings.event import GameRescheduledEvent
from fbsrankings.infrastructure.memory.storage import GameDto
from fbsrankings.infrastructure.memory.storage import GameStorage


class GameRepository(BaseRepository, ContextManager["GameRepository"]):
    def __init__(self, storage: GameStorage, bus: EventBus) -> None:
        super().__init__(bus)
        self._storage = storage

        self._bus.register_handler(GameCreatedEvent, self._handle_game_created)
        self._bus.register_handler(GameRescheduledEvent, self._handle_game_rescheduled)
        self._bus.register_handler(GameCanceledEvent, self._handle_game_canceled)
        self._bus.register_handler(GameCompletedEvent, self._handle_game_completed)
        self._bus.register_handler(
            GameNotesUpdatedEvent,
            self._handle_game_notes_updated,
        )

    def close(self) -> None:
        self._bus.unregister_handler(GameCreatedEvent, self._handle_game_created)
        self._bus.unregister_handler(
            GameRescheduledEvent,
            self._handle_game_rescheduled,
        )
        self._bus.unregister_handler(GameCanceledEvent, self._handle_game_canceled)
        self._bus.unregister_handler(GameCompletedEvent, self._handle_game_completed)
        self._bus.unregister_handler(
            GameNotesUpdatedEvent,
            self._handle_game_notes_updated,
        )

    def get(self, id_: GameID) -> Optional[Game]:
        dto = self._storage.get(id_.value)
        return self._to_game(dto) if dto is not None else None

    def find(
        self,
        season_id: SeasonID,
        week: int,
        team1_id: TeamID,
        team2_id: TeamID,
    ) -> Optional[Game]:
        dto = self._storage.find(season_id.value, week, team1_id.value, team2_id.value)
        return self._to_game(dto) if dto is not None else None

    def for_season(self, season_id: SeasonID) -> List[Game]:
        dtos = self._storage.for_season(season_id.value)
        return [self._to_game(dto) for dto in dtos if dto is not None]

    def _to_game(self, dto: GameDto) -> Game:
        return Game(
            self._bus,
            GameID(dto.id_),
            SeasonID(dto.season_id),
            dto.week,
            dto.date,
            SeasonSection[dto.season_section],
            TeamID(dto.home_team_id),
            TeamID(dto.away_team_id),
            dto.home_team_score,
            dto.away_team_score,
            GameStatus[dto.status],
            dto.notes,
        )

    def _handle_game_created(self, event: GameCreatedEvent) -> None:
        self._storage.add(
            GameDto(
                event.id_,
                event.season_id,
                event.week,
                event.date,
                event.season_section,
                event.home_team_id,
                event.away_team_id,
                None,
                None,
                GameStatus.SCHEDULED.name,
                event.notes,
            ),
        )

    def _handle_game_rescheduled(self, event: GameRescheduledEvent) -> None:
        dto = self._storage.get(event.id_)
        if dto is not None:
            dto.week = event.week
            dto.date = event.date

    def _handle_game_canceled(self, event: GameCanceledEvent) -> None:
        dto = self._storage.get(event.id_)
        if dto is not None:
            dto.status = GameStatus.CANCELED.name

    def _handle_game_completed(self, event: GameCompletedEvent) -> None:
        dto = self._storage.get(event.id_)
        if dto is not None:
            dto.home_team_score = event.home_team_score
            dto.away_team_score = event.away_team_score
            dto.status = GameStatus.COMPLETED.name

    def _handle_game_notes_updated(self, event: GameNotesUpdatedEvent) -> None:
        dto = self._storage.get(event.id_)
        if dto is not None:
            dto.notes = event.notes

    def __enter__(self) -> "GameRepository":
        return self

    def __exit__(
        self,
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        return False
