import sqlite3
from datetime import datetime
from typing import Optional
from typing import Tuple
from uuid import UUID

from pypika import Parameter
from pypika import Query
from pypika.queries import QueryBuilder

from fbsrankings.common import EventBus
from fbsrankings.core.command.domain.model.game import Game
from fbsrankings.core.command.domain.model.game import (
    GameEventHandler as BaseEventHandler,
)
from fbsrankings.core.command.domain.model.game import GameID
from fbsrankings.core.command.domain.model.game import GameRepository as BaseRepository
from fbsrankings.core.command.domain.model.season import SeasonID
from fbsrankings.core.command.domain.model.team import TeamID
from fbsrankings.core.command.event.game import GameCanceledEvent
from fbsrankings.core.command.event.game import GameCompletedEvent
from fbsrankings.core.command.event.game import GameCreatedEvent
from fbsrankings.core.command.event.game import GameNotesUpdatedEvent
from fbsrankings.core.command.event.game import GameRescheduledEvent
from fbsrankings.enum import GameStatus
from fbsrankings.enum import SeasonSection
from fbsrankings.storage.sqlite import GameTable


class GameRepository(BaseRepository):
    def __init__(self, connection: sqlite3.Connection, bus: EventBus) -> None:
        super().__init__(bus)
        self._connection = connection
        self._table = GameTable().table

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
        self,
        season_id: SeasonID,
        week: int,
        team1_id: TeamID,
        team2_id: TeamID,
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

    def _query(self) -> QueryBuilder:
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
    def __init__(self, cursor: sqlite3.Cursor, bus: EventBus) -> None:
        super().__init__(bus)
        self._cursor = cursor
        self._table = GameTable().table

    def handle_created(self, event: GameCreatedEvent) -> None:
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

    def handle_rescheduled(self, event: GameRescheduledEvent) -> None:
        self._cursor.execute(
            Query.update(self._table)
            .set(self._table.Week, Parameter("?"))
            .set(self._table.Date, Parameter("?"))
            .where(self._table.UUID == Parameter("?"))
            .get_sql(),
            [event.week, event.date, str(event.id_)],
        )

    def handle_canceled(self, event: GameCanceledEvent) -> None:
        self._cursor.execute(
            Query.update(self._table)
            .set(self._table.Status, Parameter("?"))
            .where(self._table.UUID == Parameter("?"))
            .get_sql(),
            [GameStatus.CANCELED.name, str(event.id_)],
        )

    def handle_completed(self, event: GameCompletedEvent) -> None:
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

    def handle_notes_updated(self, event: GameNotesUpdatedEvent) -> None:
        self._cursor.execute(
            Query.update(self._table)
            .set(self._table.Notes, Parameter("?"))
            .where(self._table.UUID == Parameter("?"))
            .get_sql(),
            [event.notes, str(event.id_)],
        )
