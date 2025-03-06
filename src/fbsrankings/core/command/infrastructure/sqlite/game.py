import sqlite3
from datetime import datetime
from typing import Optional
from typing import Tuple
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
from fbsrankings.storage.sqlite import GameTable


class GameRepository(BaseRepository):
    def __init__(self, connection: sqlite3.Connection, bus: EventBus) -> None:
        self._connection = connection
        self._table = GameTable().table
        self._bus = bus

    def get(self, id_: GameID) -> Optional[Game]:
        cursor = self._connection.cursor()
        cursor.execute(
            self._query() + " WHERE UUID = ?;",
            [str(id_)],
        )
        row = cursor.fetchone()
        cursor.close()

        return self._to_game(row) if row is not None else None

    def find(
        self,
        season_id: SeasonID,
        week: int,
        team1_id: TeamID,
        team2_id: TeamID,
    ) -> Optional[Game]:
        cursor = self._connection.cursor()
        cursor.execute(
            self._query() + " WHERE "
            "SeasonID = ? AND Week = ? "
            "AND ((HomeTeamID = ? AND AwayTeamID = ?) "
            "OR (AwayTeamID = ? AND HomeTeamID = ?));",
            [
                str(season_id),
                week,
                str(team1_id),
                str(team2_id),
                str(team1_id),
                str(team2_id),
            ],
        )
        row = cursor.fetchone()
        cursor.close()

        return self._to_game(row) if row is not None else None

    def _query(self) -> str:
        return (
            "SELECT "
            "UUID, "
            "SeasonID, "
            "Week, "
            "Date, "
            "SeasonSection, "
            "HomeTeamID, "
            "AwayTeamID, "
            "HomeTeamScore, "
            "AwayTeamScore, "
            "Status, "
            "Notes "
            f"FROM {self._table}"
        )

    def _to_game(
        self,
        row: Tuple[
            str,
            str,
            int,
            str,
            str,
            str,
            str,
            Optional[int],
            Optional[int],
            str,
            str,
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


class GameEventHandler(BaseEventHandler):
    def __init__(self, cursor: sqlite3.Cursor) -> None:
        self._cursor = cursor
        self._table = GameTable().table

    def handle_created(self, event: GameCreatedEvent) -> None:
        self._cursor.execute(
            f"INSERT INTO {self._table} ("
            "UUID, "
            "SeasonID, "
            "Week, "
            "Date, "
            "SeasonSection, "
            "HomeTeamID, "
            "AwayTeamID, "
            "HomeTeamScore, "
            "AwayTeamScore, "
            "Status, "
            "Notes) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?);",
            [
                str(event.game_id),
                str(event.season_id),
                event.week,
                event.date.strftime("%Y-%m-%d"),
                event.season_section,
                str(event.home_team_id),
                str(event.away_team_id),
                None,
                None,
                GameStatus.SCHEDULED.name,
                event.notes,
            ],
        )

    def handle_rescheduled(self, event: GameRescheduledEvent) -> None:
        self._cursor.execute(
            f"UPDATE {self._table} SET Week = ?, Date = ? WHERE UUID = ?;",
            [event.week, event.date.strftime("%Y-%m-%d"), str(event.game_id)],
        )

    def handle_canceled(self, event: GameCanceledEvent) -> None:
        self._cursor.execute(
            f"UPDATE {self._table} SET Status = ? WHERE UUID = ?;",
            [GameStatus.CANCELED.name, str(event.game_id)],
        )

    def handle_completed(self, event: GameCompletedEvent) -> None:
        self._cursor.execute(
            f"UPDATE {self._table} "
            "SET HomeTeamScore = ?, AwayTeamScore = ?, Status = ? "
            "WHERE UUID = ?;",
            [
                event.home_team_score,
                event.away_team_score,
                GameStatus.COMPLETED.name,
                str(event.game_id),
            ],
        )

    def handle_notes_updated(self, event: GameNotesUpdatedEvent) -> None:
        self._cursor.execute(
            f"UPDATE {self._table} SET Notes = ? WHERE UUID = ?;",
            [event.notes, str(event.game_id)],
        )
