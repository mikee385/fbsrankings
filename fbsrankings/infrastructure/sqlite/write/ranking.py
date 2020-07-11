import sqlite3
from typing import Any
from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple
from uuid import UUID

from typing_extensions import Protocol

from fbsrankings.common import EventBus
from fbsrankings.common import Identifier
from fbsrankings.domain import GameID
from fbsrankings.domain import Ranking
from fbsrankings.domain import RankingID
from fbsrankings.domain import RankingRepository as BaseRepository
from fbsrankings.domain import RankingType
from fbsrankings.domain import RankingValue
from fbsrankings.event import RankingCalculatedEvent
from fbsrankings.event import RankingValue as EventValue
from fbsrankings.domain import SeasonID
from fbsrankings.domain import TeamID
from fbsrankings.infrastructure.sqlite.storage import GameRankingValueTable
from fbsrankings.infrastructure.sqlite.storage import RankingTable
from fbsrankings.infrastructure.sqlite.storage import TeamRankingValueTable


class ValueTable(Protocol):
    name: str
    columns: str


class RankingRepository(BaseRepository):
    def __init__(
        self, connection: sqlite3.Connection, cursor: sqlite3.Cursor, bus: EventBus
    ) -> None:
        super().__init__(bus)

        self._connection = connection
        self._cursor = cursor

        self.table = RankingTable()
        bus.register_handler(RankingCalculatedEvent, self._handle_ranking_calculated)

    def get(self, ID: RankingID) -> Optional[Ranking[Any]]:
        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT {self.table.columns} FROM {self.table.name} WHERE UUID=?",
            [str(ID.value)],
        )
        row = cursor.fetchone()
        cursor.close()

        return self._to_ranking(row) if row is not None else None

    def find(
        self, name: str, season_ID: SeasonID, week: Optional[int]
    ) -> Optional[Ranking[Any]]:
        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT {self.table.columns} FROM {self.table.name} WHERE Name=? AND SeasonID=? AND Week=?",
            [
                name,
                str(season_ID.value),
                week,
            ],
        )
        row = cursor.fetchone()
        cursor.close()

        return self._to_ranking(row) if row is not None else None

    def for_season(self, name: str, season_ID: SeasonID) -> List[Ranking[Any]]:
        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT {self.table.columns} FROM {self.table.name} WHERE Name=? AND SeasonID=?",
            [name, str(season_ID.value)],
        )
        rows = cursor.fetchall()
        cursor.close()

        return [self._to_ranking(row) for row in rows if row is not None]
        
    def _to_ranking(
        self,
        row: Tuple[
            str, str, str, str, Optional[int],
        ],
    ) -> Ranking[Any]:
        ID = RankingID(UUID(row[0]))
        type = row[2]
        values = self._get_values(type, ID.value)
        
        return Ranking[Any](
            self._bus,
            ID,
            row[1],
            RankingType[type],
            SeasonID(UUID(row[3])),
            row[4],
            values,
        )

    def _handle_ranking_calculated(self, event: RankingCalculatedEvent) -> None:
        self._delete_values(event.type, event.ID)
            
        self._cursor.execute(
            f"DELETE FROM {self.table.name} WHERE Name=? AND SeasonID=? AND Week=?",
            [
                event.name,
                str(event.season_ID),
                event.week,
            ],
        )
        self._cursor.execute(
            f"INSERT INTO {self.table.name} ({self.table.columns}) VALUES (?, ?, ?, ?, ?)",
            [
                str(event.ID),
                event.name,
                event.type,
                str(event.season_ID),
                event.week,
            ],
        )
        
        self._create_values(event.type, event.ID, event.values)
        
    def _get_values(self, type: str, ID: UUID) -> List[RankingValue[Any]]:
        value_table = self._value_table(type)
        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT {value_table.columns} FROM {value_table.name} WHERE UUID=?",
            [str(ID)],
        )
        rows = cursor.fetchall()
        cursor.close()

        return [self._to_value(type, row) for row in rows if row is not None]
        
    def _create_values(self, type: str, ID: UUID, values: Iterable[EventValue]) -> None:
        value_table = self._value_table(type)
        for value in values:
            self._cursor.execute(
                f"INSERT INTO {value_table.name} ({value_table.columns}) VALUES (?, ?, ?, ?, ?)",
                [
                    str(ID),
                    str(value.ID),
                    value.order,
                    value.rank,
                    value.value,
                ],
            )
        
    def _delete_values(self, type: str, ID: UUID) -> None:
        value_table = self._value_table(type)
        self._cursor.execute(
            f"DELETE FROM {value_table.name} WHERE UUID=?",
            [
                str(ID),
            ],
        )
        
    def _to_value(self, type: str, row: Tuple[str, int, int, float]) -> RankingValue[Any]:
        return RankingValue[Any](
            self._value_ID(type, UUID(row[1])),
            row[2],
            row[3],
            row[4],
        )
        
    def _value_table(self, type: str) -> ValueTable:
        if type == RankingType.TEAM.name:
            return TeamRankingValueTable()
        elif type == RankingType.GAME.name:
            return GameRankingValueTable()
        else:
            raise ValueError(f"Unknown ranking type: {type}")
    
    def _value_ID(self, type: str, ID: UUID) -> Identifier:
        if type == RankingType.TEAM.name:
            return TeamID(ID)
        elif type == RankingType.GAME.name:
            return GameID(ID)
        else:
            raise ValueError(f"Unknown ranking type: {type}")

