import sqlite3
from abc import ABCMeta
from abc import abstractmethod
from typing import Generic
from typing import List
from typing import Optional
from typing import Tuple
from typing import TypeVar
from typing import Union
from uuid import UUID

from typing_extensions import Protocol

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


class RankingValueTable(Protocol):
    name: str
    columns: str


class RankingRepository(Generic[T], metaclass=ABCMeta):
    def __init__(
        self, connection: sqlite3.Connection, cursor: sqlite3.Cursor, bus: EventBus
    ) -> None:
        self._bus = bus
        self._connection = connection
        self._cursor = cursor

        self.ranking_table = RankingTable()

    @property
    @abstractmethod
    def type(self) -> RankingType:
        raise NotImplementedError

    @property
    @abstractmethod
    def value_table(self) -> RankingValueTable:
        raise NotImplementedError

    def get(self, ID: RankingID) -> Optional[Ranking[T]]:
        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT {self.ranking_table.columns} FROM {self.ranking_table.name} WHERE UUID=? AND Type=?",
            [str(ID.value), self.type.name],
        )
        row = cursor.fetchone()
        cursor.close()

        return self._to_ranking(row) if row is not None else None

    def find(
        self, name: str, season_ID: SeasonID, week: Optional[int]
    ) -> Optional[Ranking[T]]:
        where = "Name=? AND Type=? AND SeasonID=?"
        params: List[SqliteParam] = [name, self.type.name, str(season_ID.value)]

        if week is not None:
            where += " AND Week=?"
            params.append(week)
        else:
            where += " AND Week is NULL"

        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT {self.ranking_table.columns} FROM {self.ranking_table.name} WHERE {where}",
            params,
        )
        row = cursor.fetchone()
        cursor.close()

        return self._to_ranking(row) if row is not None else None

    def _to_ranking(self, row: Tuple[str, str, str, str, Optional[int]],) -> Ranking[T]:
        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT {self.value_table.columns} FROM {self.value_table.name} WHERE RankingID=?",
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

    @abstractmethod
    def _to_value(self, row: Tuple[str, str, int, int, float]) -> RankingValue[T]:
        raise NotImplementedError

    def _handle_ranking_calculated(self, event: RankingCalculatedEvent) -> None:
        where = "Name=? AND SeasonID=?"
        params: List[SqliteParam] = [event.name, str(event.season_ID)]

        if event.week is not None:
            where += " AND Week=?"
            params.append(event.week)
        else:
            where += " AND Week is NULL"

        self._cursor.execute(
            f"SELECT UUID FROM {self.ranking_table.name} WHERE {where}", params,
        )
        row = self._cursor.fetchone()
        if row is not None:
            self._cursor.execute(
                f"DELETE FROM {self.value_table.name} WHERE RankingID=?", [row[0]],
            )
            self._cursor.execute(
                f"DELETE FROM {self.ranking_table.name} WHERE UUID=?", [row[0]],
            )

        self._cursor.execute(
            f"INSERT INTO {self.ranking_table.name} ({self.ranking_table.columns}) VALUES (?, ?, ?, ?, ?)",
            [
                str(event.ID),
                event.name,
                self.type.name,
                str(event.season_ID),
                event.week,
            ],
        )
        for value in event.values:
            self._cursor.execute(
                f"INSERT INTO {self.value_table.name} ({self.value_table.columns}) VALUES (?, ?, ?, ?, ?)",
                [str(event.ID), str(value.ID), value.order, value.rank, value.value],
            )


class TeamRankingRepository(RankingRepository[TeamID], BaseTeamRankingRepository):
    def __init__(
        self, connection: sqlite3.Connection, cursor: sqlite3.Cursor, bus: EventBus
    ) -> None:
        RankingRepository.__init__(self, connection, cursor, bus)
        BaseTeamRankingRepository.__init__(self, bus)

        self._value_table = TeamRankingValueTable()

        bus.register_handler(
            TeamRankingCalculatedEvent, self._handle_ranking_calculated
        )

    @property
    def type(self) -> RankingType:
        return RankingType.TEAM

    @property
    def value_table(self) -> RankingValueTable:
        return self._value_table

    def _to_value(self, row: Tuple[str, str, int, int, float]) -> RankingValue[TeamID]:
        return RankingValue[TeamID](TeamID(UUID(row[1])), row[2], row[3], row[4],)


class GameRankingRepository(RankingRepository[GameID], BaseGameRankingRepository):
    def __init__(
        self, connection: sqlite3.Connection, cursor: sqlite3.Cursor, bus: EventBus
    ) -> None:
        RankingRepository.__init__(self, connection, cursor, bus)
        BaseGameRankingRepository.__init__(self, bus)

        self._value_table = GameRankingValueTable()

        bus.register_handler(
            GameRankingCalculatedEvent, self._handle_ranking_calculated
        )

    @property
    def type(self) -> RankingType:
        return RankingType.GAME

    @property
    def value_table(self) -> RankingValueTable:
        return self._value_table

    def _to_value(self, row: Tuple[str, str, int, int, float]) -> RankingValue[GameID]:
        return RankingValue[GameID](GameID(UUID(row[1])), row[2], row[3], row[4],)
