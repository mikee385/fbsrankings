import sqlite3
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union
from uuid import UUID

from pypika import Parameter
from pypika import Query
from pypika.queries import QueryBuilder

from fbsrankings.common import EventBus
from fbsrankings.ranking.command.domain.model.core import SeasonID
from fbsrankings.ranking.command.domain.model.core import TeamID
from fbsrankings.ranking.command.domain.model.record import TeamRecord
from fbsrankings.ranking.command.domain.model.record import (
    TeamRecordEventHandler as BaseEventHandler,
)
from fbsrankings.ranking.command.domain.model.record import TeamRecordID
from fbsrankings.ranking.command.domain.model.record import (
    TeamRecordRepository as BaseRepository,
)
from fbsrankings.ranking.command.domain.model.record import TeamRecordValue
from fbsrankings.ranking.command.event.record import TeamRecordCalculatedEvent
from fbsrankings.storage.sqlite import TeamRecordTable
from fbsrankings.storage.sqlite import TeamRecordValueTable


SqliteParam = Union[None, int, float, str, bytes]


class TeamRecordRepository(BaseRepository):
    def __init__(self, connection: sqlite3.Connection, bus: EventBus) -> None:
        super().__init__(bus)
        self._connection = connection
        self._record_table = TeamRecordTable().table
        self._value_table = TeamRecordValueTable().table

    def get(self, id_: TeamRecordID) -> Optional[TeamRecord]:
        cursor = self._connection.cursor()
        cursor.execute(
            self._query().where(self._record_table.UUID == Parameter("?")).get_sql(),
            [str(id_.value)],
        )
        row = cursor.fetchone()
        cursor.close()

        return self._to_record(row) if row is not None else None

    def find(self, season_id: SeasonID, week: Optional[int]) -> Optional[TeamRecord]:
        query = self._query().where(self._record_table.SeasonID == Parameter("?"))
        params: List[SqliteParam] = [str(season_id.value)]

        if week is not None:
            query = query.where(self._record_table.Week == Parameter("?"))
            params.append(week)
        else:
            query = query.where(self._record_table.Week.isnull())

        cursor = self._connection.cursor()
        cursor.execute(
            query.get_sql(),
            params,
        )
        row = cursor.fetchone()
        cursor.close()

        return self._to_record(row) if row is not None else None

    def _query(self) -> QueryBuilder:
        return Query.from_(self._record_table).select(
            self._record_table.UUID,
            self._record_table.SeasonID,
            self._record_table.Week,
        )

    def _to_record(self, row: Tuple[str, str, Optional[int]]) -> TeamRecord:
        cursor = self._connection.cursor()
        cursor.execute(
            Query.from_(self._value_table)
            .select(
                self._value_table.TeamRecordID,
                self._value_table.TeamID,
                self._value_table.Wins,
                self._value_table.Losses,
            )
            .where(self._value_table.TeamRecordID == Parameter("?"))
            .get_sql(),
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
    def __init__(self, cursor: sqlite3.Cursor, bus: EventBus) -> None:
        super().__init__(bus)
        self._cursor = cursor
        self._record_table = TeamRecordTable().table
        self._value_table = TeamRecordValueTable().table

    def handle_calculated(self, event: TeamRecordCalculatedEvent) -> None:
        query = (
            Query.from_(self._record_table)
            .select(self._record_table.UUID)
            .where(self._record_table.SeasonID == Parameter("?"))
        )
        params: List[SqliteParam] = [str(event.season_id)]

        if event.week is not None:
            query = query.where(self._record_table.Week == Parameter("?"))
            params.append(event.week)
        else:
            query = query.where(self._record_table.Week.isnull())

        self._cursor.execute(
            query.get_sql(),
            params,
        )
        row = self._cursor.fetchone()
        if row is not None:
            self._cursor.execute(
                Query.from_(self._value_table)
                .delete()
                .where(self._value_table.TeamRecordID == Parameter("?"))
                .get_sql(),
                [row[0]],
            )
            self._cursor.execute(
                Query.from_(self._record_table)
                .delete()
                .where(self._record_table.UUID == Parameter("?"))
                .get_sql(),
                [row[0]],
            )

        self._cursor.execute(
            Query.into(self._record_table)
            .columns(
                self._record_table.UUID,
                self._record_table.SeasonID,
                self._record_table.Week,
            )
            .insert(Parameter("?"), Parameter("?"), Parameter("?"))
            .get_sql(),
            [str(event.id_), str(event.season_id), event.week],
        )
        insert_sql = (
            Query.into(self._value_table)
            .columns(
                self._value_table.TeamRecordID,
                self._value_table.TeamID,
                self._value_table.Wins,
                self._value_table.Losses,
            )
            .insert(Parameter("?"), Parameter("?"), Parameter("?"), Parameter("?"))
            .get_sql()
        )
        for value in event.values:
            self._cursor.execute(
                insert_sql,
                [str(event.id_), str(value.team_id), value.wins, value.losses],
            )
