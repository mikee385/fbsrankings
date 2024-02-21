import sqlite3
from datetime import datetime
from typing import List
from typing import Optional
from typing import Union
from uuid import UUID

from pypika import Parameter
from pypika import Query

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


class GameRankingBySeasonWeekQueryHandler:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self._ranking_table = RankingTable().table
        self._value_table = GameRankingValueTable().table
        self._season_table = SeasonTable().table
        self._team_table = TeamTable().table
        self._game_table = GameTable().table

    def __call__(
        self,
        query: GameRankingBySeasonWeekQuery,
    ) -> Optional[GameRankingBySeasonWeekResult]:
        sql_query = (
            Query.from_(self._ranking_table)
            .select(
                self._ranking_table.UUID,
                self._ranking_table.Name,
                self._ranking_table.SeasonID,
                self._season_table.Year,
                self._ranking_table.Week,
            )
            .inner_join(self._season_table)
            .on(self._season_table.UUID == self._ranking_table.SeasonID)
            .where(
                (self._ranking_table.Name == Parameter("?"))
                & (self._ranking_table.Type == Parameter("?"))
                & (self._ranking_table.SeasonID == Parameter("?")),
            )
        )

        params: List[SqliteParam] = [
            query.name,
            RankingType.GAME.name,
            str(query.season_id),
        ]

        if query.week is not None:
            sql_query = sql_query.where(self._ranking_table.Week == Parameter("?"))
            params.append(query.week)
        else:
            sql_query = sql_query.where(self._ranking_table.Week.isnull())

        cursor = self._connection.cursor()
        cursor.execute(sql_query.get_sql(), params)
        row = cursor.fetchone()

        values = []
        if row is not None:
            home_team_table = self._team_table.as_("home_team")
            away_team_table = self._team_table.as_("away_team")

            cursor.execute(
                Query.from_(self._value_table)
                .select(
                    self._value_table.GameID,
                    self._game_table.SeasonID,
                    self._season_table.Year,
                    self._game_table.Week,
                    self._game_table.Date,
                    self._game_table.SeasonSection,
                    self._game_table.HomeTeamID,
                    home_team_table.Name,
                    self._game_table.AwayTeamID,
                    away_team_table.name,
                    self._game_table.HomeTeamScore,
                    self._game_table.AwayTeamScore,
                    self._game_table.Status,
                    self._game_table.Notes,
                    self._value_table.Ord,
                    self._value_table.Rank,
                    self._value_table.Value,
                )
                .inner_join(self._game_table)
                .on(self._game_table.UUID == self._value_table.GameID)
                .inner_join(self._season_table)
                .on(self._season_table.UUID == self._game_table.SeasonID)
                .inner_join(home_team_table)
                .on(home_team_table.UUID == self._game_table.HomeTeamID)
                .inner_join(away_team_table)
                .on(away_team_table.UUID == self._game_table.AwayTeamID)
                .where(self._value_table.RankingID == Parameter("?"))
                .get_sql(),
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
                UUID(row[0]),
                row[1],
                UUID(row[2]),
                row[3],
                row[4],
                values,
            )
        return None
