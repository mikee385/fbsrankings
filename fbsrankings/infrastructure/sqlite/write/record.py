import sqlite3
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union
from uuid import UUID

from fbsrankings.common import EventBus
from fbsrankings.domain import SeasonID
from fbsrankings.domain import TeamID
from fbsrankings.domain import TeamRecord
from fbsrankings.domain import TeamRecordID
from fbsrankings.domain import TeamRecordRepository as BaseRepository
from fbsrankings.domain import TeamRecordValue
from fbsrankings.event import TeamRecordCalculatedEvent
from fbsrankings.infrastructure.sqlite.storage import TeamRecordTable
from fbsrankings.infrastructure.sqlite.storage import TeamRecordValueTable


SqliteParam = Union[None, int, float, str, bytes]


class TeamRecordRepository(BaseRepository):
    def __init__(
        self, connection: sqlite3.Connection, cursor: sqlite3.Cursor, bus: EventBus
    ) -> None:
        self._bus = bus
        self._connection = connection
        self._cursor = cursor

        self.record_table = TeamRecordTable()
        self.value_table = TeamRecordValueTable()

        bus.register_handler(TeamRecordCalculatedEvent, self._handle_record_calculated)

    def get(self, ID: TeamRecordID) -> Optional[TeamRecord]:
        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT {self.record_table.columns} FROM {self.record_table.name} WHERE UUID=?",
            [str(ID.value)],
        )
        row = cursor.fetchone()
        cursor.close()

        return self._to_record(row) if row is not None else None

    def find(self, season_ID: SeasonID, week: Optional[int]) -> Optional[TeamRecord]:
        where = "SeasonID=?"
        params: List[SqliteParam] = [str(season_ID.value)]

        if week is not None:
            where += " AND Week=?"
            params.append(week)
        else:
            where += " AND Week is NULL"

        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT {self.record_table.columns} FROM {self.record_table.name} WHERE {where}",
            params,
        )
        row = cursor.fetchone()
        cursor.close()

        return self._to_record(row) if row is not None else None

    def _to_record(self, row: Tuple[str, str, Optional[int]],) -> TeamRecord:
        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT {self.value_table.columns} FROM {self.value_table.name} WHERE TeamRecordID=?",
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

    def _to_value(self, row: Tuple[str, str, int, int]) -> TeamRecordValue:
        return TeamRecordValue(TeamID(UUID(row[1])), row[2], row[3],)

    def _handle_record_calculated(self, event: TeamRecordCalculatedEvent) -> None:
        where = "SeasonID=?"
        params: List[SqliteParam] = [str(event.season_ID)]

        if event.week is not None:
            where += " AND Week=?"
            params.append(event.week)
        else:
            where += " AND Week is NULL"

        self._cursor.execute(
            f"SELECT UUID FROM {self.record_table.name} WHERE {where}", params,
        )
        row = self._cursor.fetchone()
        if row is not None:
            self._cursor.execute(
                f"DELETE FROM {self.value_table.name} WHERE TeamRecordID=?", [row[0]],
            )
            self._cursor.execute(
                f"DELETE FROM {self.record_table.name} WHERE UUID=?", [row[0]],
            )

        self._cursor.execute(
            f"INSERT INTO {self.record_table.name} ({self.record_table.columns}) VALUES (?, ?, ?)",
            [str(event.ID), str(event.season_ID), event.week],
        )
        for value in event.values:
            self._cursor.execute(
                f"INSERT INTO {self.value_table.name} ({self.value_table.columns}) VALUES (?, ?, ?, ?)",
                [str(event.ID), str(value.team_ID), value.wins, value.losses],
            )
