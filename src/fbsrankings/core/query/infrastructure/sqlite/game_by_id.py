import sqlite3
from datetime import datetime
from typing import Optional
from uuid import UUID

from pypika import Parameter
from pypika import Query

from fbsrankings.shared.query import GameByIDQuery
from fbsrankings.shared.query import GameByIDResult
from fbsrankings.storage.sqlite import GameTable
from fbsrankings.storage.sqlite import SeasonTable
from fbsrankings.storage.sqlite import TeamTable


class GameByIDQueryHandler:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self._season_table = SeasonTable().table
        self._team_table = TeamTable().table
        self._game_table = GameTable().table

    def __call__(self, query: GameByIDQuery) -> Optional[GameByIDResult]:
        home_team_table = self._team_table.as_("home_team")
        away_team_table = self._team_table.as_("away_team")

        cursor = self._connection.cursor()
        cursor.execute(
            Query.from_(self._game_table)
            .select(
                self._game_table.UUID,
                self._game_table.SeasonID,
                self._season_table.Year,
                self._game_table.Week,
                self._game_table.Date,
                self._game_table.SeasonSection,
                self._game_table.HomeTeamID,
                home_team_table.Name,
                self._game_table.AwayTeamID,
                away_team_table.Name,
                self._game_table.HomeTeamScore,
                self._game_table.AwayTeamScore,
                self._game_table.Status,
                self._game_table.Notes,
            )
            .inner_join(self._season_table)
            .on(self._season_table.UUID == self._game_table.SeasonID)
            .inner_join(home_team_table)
            .on(home_team_table.UUID == self._game_table.HomeTeamID)
            .inner_join(away_team_table)
            .on(away_team_table.UUID == self._game_table.AwayTeamID)
            .where(self._game_table.UUID == Parameter("?"))
            .get_sql(),
            [str(query.id_)],
        )
        row = cursor.fetchone()
        cursor.close()

        if row:
            return GameByIDResult(
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
                row[11],
                row[12],
                row[13],
            )
        return None
