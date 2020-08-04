from typing import List
from typing import Optional

from fbsrankings.common import Event
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


class GameRepository(BaseRepository):
    def __init__(self, storage: GameStorage, bus: EventBus) -> None:
        super().__init__(bus)
        self._storage = storage

    def get(self, id: GameID) -> Optional[Game]:
        dto = self._storage.get(id.value)
        return self._to_game(dto) if dto is not None else None

    def find(
        self, season_id: SeasonID, week: int, team1_id: TeamID, team2_id: TeamID,
    ) -> Optional[Game]:
        dto = self._storage.find(season_id.value, week, team1_id.value, team2_id.value)
        return self._to_game(dto) if dto is not None else None

    def for_season(self, season_id: SeasonID) -> List[Game]:
        dtos = self._storage.for_season(season_id.value)
        return [self._to_game(dto) for dto in dtos if dto is not None]

    def _to_game(self, dto: GameDto) -> Game:
        return Game(
            self._bus,
            GameID(dto.id),
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

    def handle(self, event: Event) -> bool:
        if isinstance(event, GameCreatedEvent):
            self._handle_game_created(event)
            return True
        if isinstance(event, GameRescheduledEvent):
            self._handle_game_rescheduled(event)
            return True
        if isinstance(event, GameCanceledEvent):
            self._handle_game_canceled(event)
            return True
        if isinstance(event, GameCompletedEvent):
            self._handle_game_completed(event)
            return True
        if isinstance(event, GameNotesUpdatedEvent):
            self._handle_game_notes_updated(event)
            return True
        return False

    def _handle_game_created(self, event: GameCreatedEvent) -> None:
        self._storage.add(
            GameDto(
                event.id,
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
        dto = self._storage.get(event.id)
        if dto is not None:
            dto.week = event.week
            dto.date = event.date

    def _handle_game_canceled(self, event: GameCanceledEvent) -> None:
        dto = self._storage.get(event.id)
        if dto is not None:
            dto.status = GameStatus.CANCELED.name

    def _handle_game_completed(self, event: GameCompletedEvent) -> None:
        dto = self._storage.get(event.id)
        if dto is not None:
            dto.home_team_score = event.home_team_score
            dto.away_team_score = event.away_team_score
            dto.status = GameStatus.COMPLETED.name

    def _handle_game_notes_updated(self, event: GameNotesUpdatedEvent) -> None:
        dto = self._storage.get(event.id)
        if dto is not None:
            dto.notes = event.notes
