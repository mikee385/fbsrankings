import sqlite3
from datetime import datetime
from typing import List
from typing import Optional
from typing import Tuple
from uuid import UUID

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
from fbsrankings.infrastructure.sqlite.storage import GameTable


class GameRepository(BaseRepository):
    def __init__(
        self, connection: sqlite3.Connection, cursor: sqlite3.Cursor, bus: EventBus
    ) -> None:
        super().__init__(bus)

        self._connection = connection
        self._cursor = cursor

        self.table = GameTable()

        bus.register_handler(GameCreatedEvent, self._handle_game_created)
        bus.register_handler(GameRescheduledEvent, self._handle_game_rescheduled)
        bus.register_handler(GameCanceledEvent, self._handle_game_canceled)
        bus.register_handler(GameCompletedEvent, self._handle_game_completed)
        bus.register_handler(GameNotesUpdatedEvent, self._handle_game_notes_updated)

    def get(self, ID: GameID) -> Optional[Game]:
        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT {self.table.columns} FROM {self.table.name} WHERE UUID=?",
            [str(ID.value)],
        )
        row = cursor.fetchone()
        cursor.close()

        return self._to_game(row) if row is not None else None

    def find(
        self, season_ID: SeasonID, week: int, team1_ID: TeamID, team2_ID: TeamID,
    ) -> Optional[Game]:
        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT {self.table.columns} FROM {self.table.name} WHERE SeasonID=? AND Week=? AND ((HomeTeamID=? AND AwayTeamID=?) OR (AwayTeamID=? AND HomeTeamID=?))",
            [
                str(season_ID.value),
                week,
                str(team1_ID.value),
                str(team2_ID.value),
                str(team1_ID.value),
                str(team2_ID.value),
            ],
        )
        row = cursor.fetchone()
        cursor.close()

        return self._to_game(row) if row is not None else None

    def for_season(self, season_ID: SeasonID) -> List[Game]:
        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT {self.table.columns} FROM {self.table.name} WHERE SeasonID=?",
            [str(season_ID.value)],
        )
        rows = cursor.fetchall()
        cursor.close()

        return [self._to_game(row) for row in rows if row is not None]

    def _to_game(
        self,
        row: Tuple[
            str, str, int, str, str, str, str, Optional[int], Optional[int], str, str,
        ],
    ) -> Game:
        return Game(
            self._bus,
            GameID(UUID(row[0])),
            SeasonID(UUID(row[1])),
            row[2],
            datetime.strptime(row[3], "%Y-%m-%d").date(),
            SeasonSection[row[4]],
            TeamID(UUID(row[5])),
            TeamID(UUID(row[6])),
            row[7],
            row[8],
            GameStatus[row[9]],
            row[10],
        )

    def _handle_game_created(self, event: GameCreatedEvent) -> None:
        self._cursor.execute(
            f"INSERT INTO {self.table.name} ({self.table.columns}) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                str(event.ID),
                str(event.season_ID),
                event.week,
                event.date,
                event.season_section,
                str(event.home_team_ID),
                str(event.away_team_ID),
                None,
                None,
                GameStatus.SCHEDULED.name,
                event.notes,
            ],
        )

    def _handle_game_rescheduled(self, event: GameRescheduledEvent) -> None:
        self._cursor.execute(
            f"UPDATE {self.table.name} SET Week=?, Date=? WHERE UUID=?",
            [event.week, event.date, str(event.ID)],
        )

    def _handle_game_canceled(self, event: GameCanceledEvent) -> None:
        self._cursor.execute(
            f"UPDATE {self.table.name} SET Status=? WHERE UUID=?",
            [GameStatus.CANCELED.name, str(event.ID)],
        )

    def _handle_game_completed(self, event: GameCompletedEvent) -> None:
        self._cursor.execute(
            f"UPDATE {self.table.name} SET HomeTeamScore=?, AwayTeamScore=?, Status=? WHERE UUID=?",
            [
                event.home_team_score,
                event.away_team_score,
                GameStatus.COMPLETED.name,
                str(event.ID),
            ],
        )

    def _handle_game_notes_updated(self, event: GameNotesUpdatedEvent) -> None:
        self._cursor.execute(
            f"UPDATE {self.table.name} SET Notes=? WHERE UUID=?",
            [event.notes, str(event.ID)],
        )
