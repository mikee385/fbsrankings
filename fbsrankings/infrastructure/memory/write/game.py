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

    def get(self, ID: GameID) -> Optional[Game]:
        dto = self._storage.get(ID.value)
        return self._to_game(dto) if dto is not None else None

    def find(
        self, season_ID: SeasonID, week: int, team1_ID: TeamID, team2_ID: TeamID,
    ) -> Optional[Game]:
        dto = self._storage.find(season_ID.value, week, team1_ID.value, team2_ID.value)
        return self._to_game(dto) if dto is not None else None

    def for_season(self, season_ID: SeasonID) -> List[Game]:
        dtos = self._storage.for_season(season_ID.value)
        return [self._to_game(dto) for dto in dtos if dto is not None]

    def _to_game(self, dto: GameDto) -> Game:
        return Game(
            self._bus,
            GameID(dto.ID),
            SeasonID(dto.season_ID),
            dto.week,
            dto.date,
            SeasonSection[dto.season_section],
            TeamID(dto.home_team_ID),
            TeamID(dto.away_team_ID),
            dto.home_team_score,
            dto.away_team_score,
            GameStatus[dto.status],
            dto.notes,
        )

    def handle(self, event: Event) -> bool:
        if isinstance(event, GameCreatedEvent):
            self._handle_game_created(event)
            return True
        elif isinstance(event, GameRescheduledEvent):
            self._handle_game_rescheduled(event)
            return True
        elif isinstance(event, GameCanceledEvent):
            self._handle_game_canceled(event)
            return True
        elif isinstance(event, GameCompletedEvent):
            self._handle_game_completed(event)
            return True
        elif isinstance(event, GameNotesUpdatedEvent):
            self._handle_game_notes_updated(event)
            return True
        else:
            return False

    def _handle_game_created(self, event: GameCreatedEvent) -> None:
        self._storage.add(
            GameDto(
                event.ID,
                event.season_ID,
                event.week,
                event.date,
                event.season_section,
                event.home_team_ID,
                event.away_team_ID,
                None,
                None,
                GameStatus.SCHEDULED.name,
                event.notes,
            ),
        )

    def _handle_game_rescheduled(self, event: GameRescheduledEvent) -> None:
        dto = self._storage.get(event.ID)
        if dto is not None:
            dto.week = event.week
            dto.date = event.date

    def _handle_game_canceled(self, event: GameCanceledEvent) -> None:
        dto = self._storage.get(event.ID)
        if dto is not None:
            dto.status = GameStatus.CANCELED.name

    def _handle_game_completed(self, event: GameCompletedEvent) -> None:
        dto = self._storage.get(event.ID)
        if dto is not None:
            dto.home_team_score = event.home_team_score
            dto.away_team_score = event.away_team_score
            dto.status = GameStatus.COMPLETED.name

    def _handle_game_notes_updated(self, event: GameNotesUpdatedEvent) -> None:
        dto = self._storage.get(event.ID)
        if dto is not None:
            dto.notes = event.notes
