import sqlite3
from datetime import datetime
from typing import List
from typing import Optional
from typing import Union
from uuid import UUID

from fbsrankings.infrastructure.sqlite.storage import GameRankingValueTable
from fbsrankings.infrastructure.sqlite.storage import GameTable
from fbsrankings.infrastructure.sqlite.storage import RankingTable
from fbsrankings.infrastructure.sqlite.storage import RankingType
from fbsrankings.infrastructure.sqlite.storage import SeasonTable
from fbsrankings.infrastructure.sqlite.storage import TeamTable
from fbsrankings.query import GameRankingBySeasonWeekQuery
from fbsrankings.query import GameRankingBySeasonWeekResult
from fbsrankings.query import GameRankingValueBySeasonWeekResult


SqliteParam = Union[None, int, float, str, bytes]


class GameRankingBySeasonWeekQueryHandler(object):
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self.ranking_table = RankingTable()
        self.value_table = GameRankingValueTable()
        self.season_table = SeasonTable()
        self.team_table = TeamTable()
        self.game_table = GameTable()

    def __call__(
        self, query: GameRankingBySeasonWeekQuery
    ) -> Optional[GameRankingBySeasonWeekResult]:
        where = "ranking.Name=? AND ranking.Type=? AND ranking.SeasonID=?"
        params: List[SqliteParam] = [
            query.name,
            RankingType.GAME.name,
            str(query.season_ID),
        ]

        if query.week is not None:
            where += " AND Week=?"
            params.append(query.week)
        else:
            where += " AND Week is NULL"

        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT ranking.UUID, "
            + "ranking.Name, "
            + "ranking.SeasonID, "
            + "season.Year, "
            + "ranking.Week "
            + f"FROM {self.ranking_table.name} AS ranking "
            + f"INNER JOIN {self.season_table.name} AS season ON season.UUID = ranking.SeasonID "
            + f"WHERE {where}",
            params,
        )
        row = cursor.fetchone()

        values = []
        if row is not None:
            cursor.execute(
                "SELECT value.GameID, "
                + "game.SeasonID, "
                + "season.Year, "
                + "game.Week, "
                + "game.Date, "
                + "game.SeasonSection, "
                + "game.HomeTeamID, "
                + "home_team.Name, "
                + "game.AwayTeamID, "
                + "away_team.name, "
                + "game.HomeTeamScore, "
                + "game.AwayTeamScore, "
                + "game.Status, "
                + "game.Notes, "
                + "value.Ord, "
                + "value.Rank, "
                + "value.Value "
                + f"FROM {self.value_table.name} AS value "
                + f"INNER JOIN {self.game_table.name} AS game ON game.UUID = value.GameID "
                + f"INNER JOIN {self.season_table.name} AS season ON season.UUID = game.SeasonID "
                + f"INNER JOIN {self.team_table.name} AS home_team ON home_team.UUID = game.HomeTeamID "
                + f"INNER JOIN {self.team_table.name} AS away_team ON away_team.UUID = game.AwayTeamID "
                + "WHERE value.RankingID=?",
                [row[0]],
            )
            values = [
                GameRankingValueBySeasonWeekResult(
                    UUID(value[0]),
                    UUID(value[1]),
                    value[2],
                    value[3],
                    datetime.strptime(value[4], "%Y-%m-%d").date(),
                    value[5],
                    UUID(value[6]),
                    value[7],
                    UUID(value[8]),
                    value[9],
                    value[10],
                    value[11],
                    value[12],
                    value[13],
                    value[14],
                    value[15],
                    value[16],
                )
                for value in cursor.fetchall()
            ]

        cursor.close()

        if row is not None:
            return GameRankingBySeasonWeekResult(
                UUID(row[0]), row[1], UUID(row[2]), row[3], row[4], values
            )
        else:
            return None
