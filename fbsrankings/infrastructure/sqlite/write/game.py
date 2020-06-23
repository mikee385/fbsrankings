import sqlite3
from datetime import datetime
from typing import Any, Optional, Union
from uuid import UUID

from fbsrankings.common import Event, EventBus
from fbsrankings.domain import Game, GameID
from fbsrankings.domain import GameRepository as BaseRepository
from fbsrankings.domain import GameStatus, Season, SeasonID, SeasonSection, Team, TeamID
from fbsrankings.event import (
    GameCanceledEvent,
    GameCompletedEvent,
    GameCreatedEvent,
    GameNotesUpdatedEvent,
    GameRescheduledEvent,
)
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
        return self._to_game(row)

    def find(
        self,
        season: Union[Season, SeasonID],
        week: int,
        team1: Union[Team, TeamID],
        team2: Union[Team, TeamID],
    ) -> Optional[Game]:
        if isinstance(season, Season):
            season_ID = season.ID
        elif isinstance(season, SeasonID):
            season_ID = season
        else:
            raise TypeError("season must be of type Season or SeasonID")

        if isinstance(team1, Team):
            team1_ID = team1.ID
        elif isinstance(team1, TeamID):
            team1_ID = team1
        else:
            raise TypeError("team1 must be of type Team or TeamID")

        if isinstance(team2, Team):
            team2_ID = team2.ID
        elif isinstance(team2, TeamID):
            team2_ID = team2
        else:
            raise TypeError("team2 must be of type Team or TeamID")

        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT {self.table.columns} FROM {self.table.name}  WHERE SeasonID=? AND Week=? AND ((HomeTeamID=? AND AwayTeamID=?) OR (AwayTeamID=? AND HomeTeamID=?))",
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
        return self._to_game(row)

    def _to_game(self, row: Any) -> Optional[Game]:
        if row is not None:
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
        else:
            return None

    def _handle_game_created(self, event: Event) -> None:
        if not isinstance(event, GameCreatedEvent):
            raise TypeError("event must be of type GameCreatedEvent")

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

    def _handle_game_rescheduled(self, event: Event) -> None:
        if not isinstance(event, GameRescheduledEvent):
            raise TypeError("event must be of type GameRescheduledEvent")

        self._cursor.execute(
            f"UPDATE {self.table.name} SET Week=?, Date=? WHERE UUID=?",
            [event.week, event.date, str(event.ID)],
        )

    def _handle_game_canceled(self, event: Event) -> None:
        if not isinstance(event, GameCanceledEvent):
            raise TypeError("event must be of type GameCanceledEvent")

        self._cursor.execute(
            f"UPDATE {self.table.name} SET Status=? WHERE UUID=?",
            [GameStatus.CANCELED.name, str(event.ID)],
        )

    def _handle_game_completed(self, event: Event) -> None:
        if not isinstance(event, GameCompletedEvent):
            raise TypeError("event must be of type GameCompletedEvent")

        self._cursor.execute(
            f"UPDATE {self.table.name} SET HomeTeamScore=?, AwayTeamScore=?, Status=? WHERE UUID=?",
            [
                event.home_team_score,
                event.away_team_score,
                GameStatus.COMPLETED.name,
                str(event.ID),
            ],
        )

    def _handle_game_notes_updated(self, event: Event) -> None:
        if not isinstance(event, GameNotesUpdatedEvent):
            raise TypeError("event must be of type GameNotesUpdatedEvent")

        self._cursor.execute(
            f"UPDATE {self.table.name} SET Notes=? WHERE UUID=?",
            [event.notes, str(event.ID)],
        )
