import sqlite3
from typing import Callable
from typing import Generic
from typing import List
from typing import Optional
from typing import Tuple
from typing import TypeVar
from typing import Union
from uuid import UUID

from pypika import Field
from pypika import Parameter
from pypika import Query
from pypika import Table

from fbsrankings.common import EventBus
from fbsrankings.common import Identifier
from fbsrankings.domain import GameID
from fbsrankings.domain import GameRankingRepository as BaseGameRankingRepository
from fbsrankings.domain import Ranking
from fbsrankings.domain import RankingID
from fbsrankings.domain import RankingValue
from fbsrankings.domain import SeasonID
from fbsrankings.domain import TeamID
from fbsrankings.domain import TeamRankingRepository as BaseTeamRankingRepository
from fbsrankings.event import GameRankingCalculatedEvent
from fbsrankings.event import RankingCalculatedEvent
from fbsrankings.event import TeamRankingCalculatedEvent
from fbsrankings.infrastructure.sqlite.storage import GameRankingValueTable
from fbsrankings.infrastructure.sqlite.storage import RankingTable
from fbsrankings.infrastructure.sqlite.storage import RankingType
from fbsrankings.infrastructure.sqlite.storage import TeamRankingValueTable


T = TypeVar("T", bound=Identifier)


SqliteParam = Union[None, int, float, str, bytes]


class RankingRepository(Generic[T]):
    def __init__(
        self,
        connection: sqlite3.Connection,
        cursor: sqlite3.Cursor,
        bus: EventBus,
        value_table: Table,
        value_columns: List[Field],
        type: RankingType,
        to_value: Callable[[Tuple[str, str, int, int, float]], RankingValue[T]],
    ) -> None:
        self._bus = bus
        self._connection = connection
        self._cursor = cursor

        self._ranking_table = RankingTable().table
        self._value_table = value_table
        self._value_columns = value_columns

        self._type = type
        self._to_value = to_value

    def get(self, id: RankingID) -> Optional[Ranking[T]]:
        cursor = self._connection.cursor()
        cursor.execute(
            self._query()
            .where(
                (self._ranking_table.UUID == Parameter("?"))
                & (self._ranking_table.Type == Parameter("?")),
            )
            .get_sql(),
            [str(id.value), self._type.name],
        )
        row = cursor.fetchone()
        cursor.close()

        return self._to_ranking(row) if row is not None else None

    def find(
        self, name: str, season_id: SeasonID, week: Optional[int],
    ) -> Optional[Ranking[T]]:
        query = self._query().where(
            (self._ranking_table.Name == Parameter("?"))
            & (self._ranking_table.Type == Parameter("?"))
            & (self._ranking_table.SeasonID == Parameter("?")),
        )
        params: List[SqliteParam] = [name, self._type.name, str(season_id.value)]

        if week is not None:
            query = query.where(self._ranking_table.Week == Parameter("?"))
            params.append(week)
        else:
            query = query.where(self._ranking_table.Week.isnull())

        cursor = self._connection.cursor()
        cursor.execute(
            query.get_sql(), params,
        )
        row = cursor.fetchone()
        cursor.close()

        return self._to_ranking(row) if row is not None else None

    def _query(self) -> Query:
        return Query.from_(self._ranking_table).select(
            self._ranking_table.UUID,
            self._ranking_table.Name,
            self._ranking_table.Type,
            self._ranking_table.SeasonID,
            self._ranking_table.Week,
        )

    def _to_ranking(self, row: Tuple[str, str, str, str, Optional[int]]) -> Ranking[T]:
        cursor = self._connection.cursor()
        cursor.execute(
            Query.from_(self._value_table)
            .select(self._value_columns)
            .where(self._value_table.RankingID == Parameter("?"))
            .get_sql(),
            [row[0]],
        )
        rows = cursor.fetchall()
        cursor.close()

        values = [self._to_value(row) for row in rows if row is not None]

        return Ranking[T](
            self._bus,
            RankingID(UUID(row[0])),
            row[1],
            SeasonID(UUID(row[3])),
            row[4],
            values,
        )

    def handle_ranking_calculated(self, event: RankingCalculatedEvent) -> None:
        query = (
            Query.from_(self._ranking_table)
            .select(self._ranking_table.UUID)
            .where(
                (self._ranking_table.Name == Parameter("?"))
                & (self._ranking_table.Type == Parameter("?"))
                & (self._ranking_table.SeasonID == Parameter("?")),
            )
        )
        params: List[SqliteParam] = [event.name, self._type.name, str(event.season_id)]

        if event.week is not None:
            query = query.where(self._ranking_table.Week == Parameter("?"))
            params.append(event.week)
        else:
            query = query.where(self._ranking_table.Week.isnull())

        self._cursor.execute(
            query.get_sql(), params,
        )
        row = self._cursor.fetchone()
        if row is not None:
            self._cursor.execute(
                Query.from_(self._value_table)
                .delete()
                .where(self._value_table.RankingID == Parameter("?"))
                .get_sql(),
                [row[0]],
            )
            self._cursor.execute(
                Query.from_(self._ranking_table)
                .delete()
                .where(self._ranking_table.UUID == Parameter("?"))
                .get_sql(),
                [row[0]],
            )

        self._cursor.execute(
            Query.into(self._ranking_table)
            .columns(
                self._ranking_table.UUID,
                self._ranking_table.Name,
                self._ranking_table.Type,
                self._ranking_table.SeasonID,
                self._ranking_table.Week,
            )
            .insert(
                Parameter("?"),
                Parameter("?"),
                Parameter("?"),
                Parameter("?"),
                Parameter("?"),
            )
            .get_sql(),
            [
                str(event.id),
                event.name,
                self._type.name,
                str(event.season_id),
                event.week,
            ],
        )
        insert_sql = (
            Query.into(self._value_table)
            .columns(self._value_columns)
            .insert(
                Parameter("?"),
                Parameter("?"),
                Parameter("?"),
                Parameter("?"),
                Parameter("?"),
            )
            .get_sql()
        )
        for value in event.values:
            self._cursor.execute(
                insert_sql,
                [str(event.id), str(value.id), value.order, value.rank, value.value],
            )


class TeamRankingRepository(BaseTeamRankingRepository):
    def __init__(
        self, connection: sqlite3.Connection, cursor: sqlite3.Cursor, bus: EventBus,
    ) -> None:
        super().__init__(bus)

        value_table = TeamRankingValueTable().table
        value_columns = [
            value_table.RankingID,
            value_table.TeamID,
            value_table.Ord,
            value_table.Rank,
            value_table.Value,
        ]
        self._repository = RankingRepository[TeamID](
            connection,
            cursor,
            bus,
            value_table,
            value_columns,
            RankingType.TEAM,
            self._to_value,
        )

        bus.register_handler(
            TeamRankingCalculatedEvent, self._repository.handle_ranking_calculated,
        )

    def get(self, id: RankingID) -> Optional[Ranking[TeamID]]:
        return self._repository.get(id)

    def find(
        self, name: str, season_id: SeasonID, week: Optional[int],
    ) -> Optional[Ranking[TeamID]]:
        return self._repository.find(name, season_id, week)

    @staticmethod
    def _to_value(row: Tuple[str, str, int, int, float]) -> RankingValue[TeamID]:
        return RankingValue[TeamID](TeamID(UUID(row[1])), row[2], row[3], row[4])


class GameRankingRepository(BaseGameRankingRepository):
    def __init__(
        self, connection: sqlite3.Connection, cursor: sqlite3.Cursor, bus: EventBus,
    ) -> None:
        super().__init__(bus)

        value_table = GameRankingValueTable().table
        value_columns = [
            value_table.RankingID,
            value_table.GameID,
            value_table.Ord,
            value_table.Rank,
            value_table.Value,
        ]
        self._repository = RankingRepository[GameID](
            connection,
            cursor,
            bus,
            value_table,
            value_columns,
            RankingType.GAME,
            self._to_value,
        )

        bus.register_handler(
            GameRankingCalculatedEvent, self._repository.handle_ranking_calculated,
        )

    def get(self, id: RankingID) -> Optional[Ranking[GameID]]:
        return self._repository.get(id)

    def find(
        self, name: str, season_id: SeasonID, week: Optional[int],
    ) -> Optional[Ranking[GameID]]:
        return self._repository.find(name, season_id, week)

    @staticmethod
    def _to_value(row: Tuple[str, str, int, int, float]) -> RankingValue[GameID]:
        return RankingValue[GameID](GameID(UUID(row[1])), row[2], row[3], row[4])
