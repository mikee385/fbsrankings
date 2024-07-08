import sqlite3
from typing import Callable
from typing import Generic
from typing import List
from typing import Optional
from typing import Tuple
from typing import TypeVar
from typing import Union
from uuid import UUID

from fbsrankings.ranking.command.domain.model.core import GameID
from fbsrankings.ranking.command.domain.model.core import SeasonID
from fbsrankings.ranking.command.domain.model.core import TeamID
from fbsrankings.ranking.command.domain.model.ranking import (
    GameRankingRepository as BaseGameRankingRepository,
)
from fbsrankings.ranking.command.domain.model.ranking import Ranking
from fbsrankings.ranking.command.domain.model.ranking import RankingID
from fbsrankings.ranking.command.domain.model.ranking import RankingValue
from fbsrankings.ranking.command.domain.model.ranking import (
    TeamRankingRepository as BaseTeamRankingRepository,
)
from fbsrankings.shared.event import GameRankingCalculatedEvent
from fbsrankings.shared.event import (
    GameRankingEventHandler as BaseGameRankingEventHandler,
)
from fbsrankings.shared.event import RankingCalculatedEvent
from fbsrankings.shared.event import TeamRankingCalculatedEvent
from fbsrankings.shared.event import (
    TeamRankingEventHandler as BaseTeamRankingEventHandler,
)
from fbsrankings.shared.messaging import EventBus
from fbsrankings.storage.sqlite import GameRankingValueTable
from fbsrankings.storage.sqlite import RankingTable
from fbsrankings.storage.sqlite import RankingType
from fbsrankings.storage.sqlite import TeamRankingValueTable


T = TypeVar("T", bound=UUID)


SqliteParam = Union[None, int, float, str, bytes]


class RankingRepository(Generic[T]):
    def __init__(
        self,
        bus: EventBus,
        connection: sqlite3.Connection,
        value_table: str,
        value_columns: List[str],
        type_: RankingType,
        to_value: Callable[[Tuple[str, str, int, int, float]], RankingValue[T]],
    ) -> None:
        self._bus = bus
        self._connection = connection

        self._ranking_table = RankingTable().table
        self._value_table = value_table
        self._value_columns = value_columns

        self._type = type_
        self._to_value = to_value

    def get(self, id_: RankingID) -> Optional[Ranking[T]]:
        cursor = self._connection.cursor()
        cursor.execute(
            self._query() + " WHERE UUID = ? AND Type = ?;",
            [str(id_), self._type.name],
        )
        row = cursor.fetchone()
        cursor.close()

        return self._to_ranking(row) if row is not None else None

    def find(
        self,
        name: str,
        season_id: SeasonID,
        week: Optional[int],
    ) -> Optional[Ranking[T]]:
        query = self._query() + " WHERE Name = ? AND Type = ? AND SeasonID = ?"
        params: List[SqliteParam] = [name, self._type.name, str(season_id)]

        if week is not None:
            query += " AND Week = ?;"
            params.append(week)
        else:
            query += " AND Week IS NULL;"

        cursor = self._connection.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        cursor.close()

        return self._to_ranking(row) if row is not None else None

    def _query(self) -> str:
        return (
            "SELECT "
            "UUID, "
            "Name, "
            "Type, "
            "SeasonID, "
            "Week "
            f"FROM {self._ranking_table}"
        )

    def _to_ranking(self, row: Tuple[str, str, str, str, Optional[int]]) -> Ranking[T]:
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT " + " ,".join(self._value_columns) + " WHERE RankingID = ?;",
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


class RankingEventHandler:
    def __init__(
        self,
        cursor: sqlite3.Cursor,
        value_table: str,
        value_columns: List[str],
        type_: RankingType,
    ) -> None:
        self._cursor = cursor
        self._ranking_table = RankingTable().table
        self._value_table = value_table
        self._value_columns = value_columns
        self._type = type_

    def handle_calculated(self, event: RankingCalculatedEvent) -> None:
        query = (
            "SELECT UUID "
            f"FROM {self._ranking_table} "
            "WHERE Name = ? AND Type = ? AND SeasonID = ?"
        )
        params: List[SqliteParam] = [event.name, self._type.name, str(event.season_id)]

        if event.week is not None:
            query += " AND Week = ?;"
            params.append(event.week)
        else:
            query += " AND Week IS NULL;"

        self._cursor.execute(query, params)
        row = self._cursor.fetchone()
        if row is not None:
            self._cursor.execute(
                f"DELETE FROM {self._value_table} WHERE RankingID = ?;",
                [row[0]],
            )
            self._cursor.execute(
                f"DELETE FROM {self._ranking_table} WHERE UUID = ?;",
                [row[0]],
            )

        self._cursor.execute(
            f"INSERT INTO {self._ranking_table} "
            "(UUID, Name, Type, SeasonID, Week) "
            "VALUES (?,?,?,?,?)",
            [
                str(event.id_),
                event.name,
                self._type.name,
                str(event.season_id),
                event.week,
            ],
        )
        insert_sql = (
            f"INSERT INTO {self._value_table} "
            "(" + ", ".join(self._value_columns) + ") "
            "VALUES (?,?,?,?,?)"
        )
        for value in event.values:
            self._cursor.execute(
                insert_sql,
                [str(event.id_), str(value.id_), value.order, value.rank, value.value],
            )


class TeamRankingRepository(BaseTeamRankingRepository):
    def __init__(self, connection: sqlite3.Connection, bus: EventBus) -> None:
        value_table = TeamRankingValueTable().table
        value_columns = [
            "RankingID",
            "TeamID",
            "Ord",
            "Rank",
            "Value",
        ]
        self._repository = RankingRepository[TeamID](
            bus,
            connection,
            value_table,
            value_columns,
            RankingType.TEAM,
            self._to_value,
        )

    def get(self, id_: RankingID) -> Optional[Ranking[TeamID]]:
        return self._repository.get(id_)

    def find(
        self,
        name: str,
        season_id: SeasonID,
        week: Optional[int],
    ) -> Optional[Ranking[TeamID]]:
        return self._repository.find(name, season_id, week)

    @staticmethod
    def _to_value(row: Tuple[str, str, int, int, float]) -> RankingValue[TeamID]:
        return RankingValue[TeamID](TeamID(UUID(row[1])), row[2], row[3], row[4])


class TeamRankingEventHandler(BaseTeamRankingEventHandler):
    def __init__(self, cursor: sqlite3.Cursor) -> None:
        value_table = TeamRankingValueTable().table
        value_columns = [
            "RankingID",
            "TeamID",
            "Ord",
            "Rank",
            "Value",
        ]
        self._event_handler = RankingEventHandler(
            cursor,
            value_table,
            value_columns,
            RankingType.TEAM,
        )

    def handle_calculated(self, event: TeamRankingCalculatedEvent) -> None:
        self._event_handler.handle_calculated(event)


class GameRankingRepository(BaseGameRankingRepository):
    def __init__(self, connection: sqlite3.Connection, bus: EventBus) -> None:
        value_table = GameRankingValueTable().table
        value_columns = [
            "RankingID",
            "GameID",
            "Ord",
            "Rank",
            "Value",
        ]
        self._repository = RankingRepository[GameID](
            bus,
            connection,
            value_table,
            value_columns,
            RankingType.GAME,
            self._to_value,
        )

    def get(self, id_: RankingID) -> Optional[Ranking[GameID]]:
        return self._repository.get(id_)

    def find(
        self,
        name: str,
        season_id: SeasonID,
        week: Optional[int],
    ) -> Optional[Ranking[GameID]]:
        return self._repository.find(name, season_id, week)

    @staticmethod
    def _to_value(row: Tuple[str, str, int, int, float]) -> RankingValue[GameID]:
        return RankingValue[GameID](GameID(UUID(row[1])), row[2], row[3], row[4])


class GameRankingEventHandler(BaseGameRankingEventHandler):
    def __init__(self, cursor: sqlite3.Cursor) -> None:
        value_table = GameRankingValueTable().table
        value_columns = [
            "RankingID",
            "GameID",
            "Ord",
            "Rank",
            "Value",
        ]
        self._event_handler = RankingEventHandler(
            cursor,
            value_table,
            value_columns,
            RankingType.GAME,
        )

    def handle_calculated(self, event: GameRankingCalculatedEvent) -> None:
        self._event_handler.handle_calculated(event)
