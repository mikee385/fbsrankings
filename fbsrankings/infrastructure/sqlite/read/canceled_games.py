import sqlite3
from datetime import datetime
from uuid import UUID

from fbsrankings.common import QueryHandler
from fbsrankings.domain import GameStatus
from fbsrankings.infrastructure.sqlite.storage import GameTable
from fbsrankings.infrastructure.sqlite.storage import SeasonTable
from fbsrankings.infrastructure.sqlite.storage import TeamTable
from fbsrankings.query import CanceledGameResult
from fbsrankings.query import CanceledGamesQuery
from fbsrankings.query import CanceledGamesResult


class CanceledGamesQueryHandler(QueryHandler[CanceledGamesQuery, CanceledGamesResult]):
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self.season_table = SeasonTable()
        self.team_table = TeamTable()
        self.game_table = GameTable()

    def handle(self, query: CanceledGamesQuery) -> CanceledGamesResult:
        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT game.UUID, game.SeasonID, season.Year, game.Week, game.Date, game.SeasonSection, game.HomeTeamID, home_team.Name, game.AwayTeamID, away_team.name, game.Notes FROM {self.game_table.name} AS game INNER JOIN {self.season_table.name} AS season ON season.UUID = game.SeasonID INNER JOIN {self.team_table.name} AS home_team ON home_team.UUID = game.HomeTeamID INNER JOIN {self.team_table.name} AS away_team ON away_team.UUID = game.AwayTeamID WHERE game.Status =?",
            [GameStatus.CANCELED.name],
        )
        items = [
            CanceledGameResult(
                UUID(row[0]),
                UUID(row[1]),
                row[2],
                row[3],
                datetime.strptime(row[4], "%Y-%m-%d").date(),
                row[5],
                UUID(row[6]),
                row[7],
                UUID(row[8]),
                row[9],
                row[10],
            )
            for row in cursor.fetchall()
        ]
        cursor.close()

        return CanceledGamesResult(items)
