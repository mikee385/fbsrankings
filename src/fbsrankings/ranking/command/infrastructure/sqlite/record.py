import sqlite3
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union
from uuid import UUID

from fbsrankings.ranking.command.domain.model.core import SeasonID
from fbsrankings.ranking.command.domain.model.core import TeamID
from fbsrankings.ranking.command.domain.model.record import TeamRecord
from fbsrankings.ranking.command.domain.model.record import TeamRecordID
from fbsrankings.ranking.command.domain.model.record import (
    TeamRecordRepository as BaseRepository,
)
from fbsrankings.ranking.command.domain.model.record import TeamRecordValue
from fbsrankings.shared.event import TeamRecordCalculatedEvent
from fbsrankings.shared.event import TeamRecordEventHandler as BaseEventHandler
from fbsrankings.shared.messaging import EventBus
from fbsrankings.storage.sqlite import TeamRecordTable
from fbsrankings.storage.sqlite import TeamRecordValueTable


SqliteParam = Union[None, int, float, str, bytes]


class TeamRecordRepository(BaseRepository):
    def __init__(self, connection: sqlite3.Connection, bus: EventBus) -> None:
        self._connection = connection
        self._record_table = TeamRecordTable().table
        self._value_table = TeamRecordValueTable().table
        self._bus = bus

    def get(self, id_: TeamRecordID) -> Optional[TeamRecord]:
        cursor = self._connection.cursor()
        cursor.execute(
            self._query() + " WHERE UUID = ?;",
            [str(id_)],
        )
        row = cursor.fetchone()
        cursor.close()

        return self._to_record(row) if row is not None else None

    def find(self, season_id: SeasonID, week: Optional[int]) -> Optional[TeamRecord]:
        query = self._query() + " WHERE SeasonID = ?"
        params: List[SqliteParam] = [str(season_id)]

        if week is not None:
            query += " AND Week = ?;"
            params.append(week)
        else:
            query += " AND Week IS NULL;"

        cursor = self._connection.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        cursor.close()

        return self._to_record(row) if row is not None else None

    def _query(self) -> str:
        return f"SELECT UUID, SeasonID, Week FROM {self._record_table}"

    def _to_record(self, row: Tuple[str, str, Optional[int]]) -> TeamRecord:
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT "
            "TeamRecordID, "
            "TeamID, "
            "Wins, "
            "Losses "
            f"FROM {self._value_table} "
            "WHERE TeamRecordID = ?;",
            [row[0]],
        )
        rows = cursor.fetchall()
        cursor.close()

        values = [self._to_value(row) for row in rows if row is not None]

        return TeamRecord(
            self._bus,
            TeamRecordID(UUID(row[0])),
            SeasonID(UUID(row[1])),
            row[2],
            values,
        )

    @staticmethod
    def _to_value(row: Tuple[str, str, int, int]) -> TeamRecordValue:
        return TeamRecordValue(TeamID(UUID(row[1])), row[2], row[3])


class TeamRecordEventHandler(BaseEventHandler):
    def __init__(self, cursor: sqlite3.Cursor) -> None:
        self._cursor = cursor
        self._record_table = TeamRecordTable().table
        self._value_table = TeamRecordValueTable().table

    def handle_calculated(self, event: TeamRecordCalculatedEvent) -> None:
        query = f"SELECT UUID FROM {self._record_table} WHERE SeasonID = ?"
        params: List[SqliteParam] = [str(event.season_id)]

        if event.week is not None:
            query += " AND Week = ?;"
            params.append(event.week)
        else:
            query += " AND Week IS NULL;"

        self._cursor.execute(query, params)
        row = self._cursor.fetchone()
        if row is not None:
            self._cursor.execute(
                f"DELETE FROM {self._value_table} WHERE TeamRecordID = ?;",
                [row[0]],
            )
            self._cursor.execute(
                f"DELETE FROM {self._record_table} WHERE UUID = ?;",
                [row[0]],
            )

        self._cursor.execute(
            f"INSERT INTO {self._record_table} "
            "(UUID, SeasonID, Week) "
            "VALUES (?,?,?);",
            [str(event.id_), str(event.season_id), event.week],
        )
        insert_sql = (
            f"INSERT INTO {self._value_table} "
            "(TeamRecordID, TeamID, Wins, Losses) "
            "VALUES (?,?,?,?);"
        )
        for value in event.values:
            self._cursor.execute(
                insert_sql,
                [str(event.id_), str(value.team_id), value.wins, value.losses],
            )
