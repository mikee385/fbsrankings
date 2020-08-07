import sqlite3
from datetime import datetime
from typing import List
from typing import Optional
from typing import Tuple
from uuid import UUID

from pypika import Parameter
from pypika import Query

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
        self, connection: sqlite3.Connection, cursor: sqlite3.Cursor, bus: EventBus,
    ) -> None:
        super().__init__(bus)

        self._connection = connection
        self._cursor = cursor

        self._table = GameTable().table

        bus.register_handler(GameCreatedEvent, self._handle_game_created)
        bus.register_handler(GameRescheduledEvent, self._handle_game_rescheduled)
        bus.register_handler(GameCanceledEvent, self._handle_game_canceled)
        bus.register_handler(GameCompletedEvent, self._handle_game_completed)
        bus.register_handler(GameNotesUpdatedEvent, self._handle_game_notes_updated)

    def get(self, id_: GameID) -> Optional[Game]:
        cursor = self._connection.cursor()
        cursor.execute(
            self._query().where(self._table.UUID == Parameter("?")).get_sql(),
            [str(id_.value)],
        )
        row = cursor.fetchone()
        cursor.close()

        return self._to_game(row) if row is not None else None

    def find(
        self, season_id: SeasonID, week: int, team1_id: TeamID, team2_id: TeamID,
    ) -> Optional[Game]:
        cursor = self._connection.cursor()
        cursor.execute(
            self._query()
            .where(self._table.SeasonID == Parameter("?"))
            .where(self._table.Week == Parameter("?"))
            .where(
                (
                    (self._table.HomeTeamID == Parameter("?"))
                    & (self._table.AwayTeamID == Parameter("?"))
                )
                | (
                    (self._table.AwayTeamID == Parameter("?"))
                    & (self._table.HomeTeamID == Parameter("?"))
                ),
            )
            .get_sql(),
            [
                str(season_id.value),
                week,
                str(team1_id.value),
                str(team2_id.value),
                str(team1_id.value),
                str(team2_id.value),
            ],
        )
        row = cursor.fetchone()
        cursor.close()

        return self._to_game(row) if row is not None else None

    def for_season(self, season_id: SeasonID) -> List[Game]:
        cursor = self._connection.cursor()
        cursor.execute(
            self._query().where(self._table.SeasonID == Parameter("?")).get_sql(),
            [str(season_id.value)],
        )
        rows = cursor.fetchall()
        cursor.close()

        return [self._to_game(row) for row in rows if row is not None]

    def _query(self) -> Query:
        return Query.from_(self._table).select(
            self._table.UUID,
            self._table.SeasonID,
            self._table.Week,
            self._table.Date,
            self._table.SeasonSection,
            self._table.HomeTeamID,
            self._table.AwayTeamID,
            self._table.HomeTeamScore,
            self._table.AwayTeamScore,
            self._table.Status,
            self._table.Notes,
        )

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
            Query.into(self._table)
            .columns(
                self._table.UUID,
                self._table.SeasonID,
                self._table.Week,
                self._table.Date,
                self._table.SeasonSection,
                self._table.HomeTeamID,
                self._table.AwayTeamID,
                self._table.HomeTeamScore,
                self._table.AwayTeamScore,
                self._table.Status,
                self._table.Notes,
            )
            .insert(
                Parameter("?"),
                Parameter("?"),
                Parameter("?"),
                Parameter("?"),
                Parameter("?"),
                Parameter("?"),
                Parameter("?"),
                Parameter("?"),
                Parameter("?"),
                Parameter("?"),
                Parameter("?"),
            )
            .get_sql(),
            [
                str(event.id_),
                str(event.season_id),
                event.week,
                event.date,
                event.season_section,
                str(event.home_team_id),
                str(event.away_team_id),
                None,
                None,
                GameStatus.SCHEDULED.name,
                event.notes,
            ],
        )

    def _handle_game_rescheduled(self, event: GameRescheduledEvent) -> None:
        self._cursor.execute(
            Query.update(self._table)
            .set(self._table.Week, Parameter("?"))
            .set(self._table.Date, Parameter("?"))
            .where(self._table.UUID == Parameter("?"))
            .get_sql(),
            [event.week, event.date, str(event.id_)],
        )

    def _handle_game_canceled(self, event: GameCanceledEvent) -> None:
        self._cursor.execute(
            Query.update(self._table)
            .set(self._table.Status, Parameter("?"))
            .where(self._table.UUID == Parameter("?"))
            .get_sql(),
            [GameStatus.CANCELED.name, str(event.id_)],
        )

    def _handle_game_completed(self, event: GameCompletedEvent) -> None:
        self._cursor.execute(
            Query.update(self._table)
            .set(self._table.HomeTeamScore, Parameter("?"))
            .set(self._table.AwayTeamScore, Parameter("?"))
            .set(self._table.Status, Parameter("?"))
            .where(self._table.UUID == Parameter("?"))
            .get_sql(),
            [
                event.home_team_score,
                event.away_team_score,
                GameStatus.COMPLETED.name,
                str(event.id_),
            ],
        )

    def _handle_game_notes_updated(self, event: GameNotesUpdatedEvent) -> None:
        self._cursor.execute(
            Query.update(self._table)
            .set(self._table.Notes, Parameter("?"))
            .where(self._table.UUID == Parameter("?"))
            .get_sql(),
            [event.notes, str(event.id_)],
        )
