from typing import Optional
from uuid import UUID

from communication.bus import EventBus
from fbsrankings.core.command.domain.model.game import Game
from fbsrankings.core.command.domain.model.game import GameID
from fbsrankings.core.command.domain.model.game import GameRepository as BaseRepository
from fbsrankings.core.command.domain.model.season import SeasonID
from fbsrankings.core.command.domain.model.team import TeamID
from fbsrankings.messages.enums import GameStatus
from fbsrankings.messages.enums import SeasonSection
from fbsrankings.messages.event import GameCanceledEvent
from fbsrankings.messages.event import GameCompletedEvent
from fbsrankings.messages.event import GameCreatedEvent
from fbsrankings.messages.event import GameEventHandler as BaseEventHandler
from fbsrankings.messages.event import GameNotesUpdatedEvent
from fbsrankings.messages.event import GameRescheduledEvent
from fbsrankings.storage.memory import GameDto
from fbsrankings.storage.memory import GameStorage


class GameRepository(BaseRepository):
    def __init__(self, storage: GameStorage, bus: EventBus) -> None:
        self._storage = storage
        self._bus = bus

    def get(self, id_: GameID) -> Optional[Game]:
        dto = self._storage.get(str(id_))
        return self._to_game(dto) if dto is not None else None

    def find(
        self,
        season_id: SeasonID,
        week: int,
        team1_id: TeamID,
        team2_id: TeamID,
    ) -> Optional[Game]:
        dto = self._storage.find(str(season_id), week, str(team1_id), str(team2_id))
        return self._to_game(dto) if dto is not None else None

    def _to_game(self, dto: GameDto) -> Game:
        return Game(
            self._bus,
            GameID(UUID(dto.id_)),
            SeasonID(UUID(dto.season_id)),
            dto.week,
            dto.date,
            SeasonSection[dto.season_section],
            TeamID(UUID(dto.home_team_id)),
            TeamID(UUID(dto.away_team_id)),
            dto.home_team_score,
            dto.away_team_score,
            GameStatus[dto.status],
            dto.notes,
        )


class GameEventHandler(BaseEventHandler):
    def __init__(self, storage: GameStorage) -> None:
        self._storage = storage

    def handle_created(self, event: GameCreatedEvent) -> None:
        self._storage.add(
            GameDto(
                event.game_id,
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

    def handle_rescheduled(self, event: GameRescheduledEvent) -> None:
        dto = self._storage.get(event.game_id)
        if dto is not None:
            dto.week = event.week
            dto.date = event.date

    def handle_canceled(self, event: GameCanceledEvent) -> None:
        dto = self._storage.get(event.game_id)
        if dto is not None:
            dto.status = GameStatus.CANCELED.name

    def handle_completed(self, event: GameCompletedEvent) -> None:
        dto = self._storage.get(event.game_id)
        if dto is not None:
            dto.home_team_score = event.home_team_score
            dto.away_team_score = event.away_team_score
            dto.status = GameStatus.COMPLETED.name

    def handle_notes_updated(self, event: GameNotesUpdatedEvent) -> None:
        dto = self._storage.get(event.game_id)
        if dto is not None:
            dto.notes = event.notes
