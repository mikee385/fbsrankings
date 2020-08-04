import sqlite3
from typing import List
from typing import Optional
from typing import Union
from uuid import UUID

from pypika import Parameter
from pypika import Query

from fbsrankings.infrastructure.sqlite.storage import RankingTable
from fbsrankings.infrastructure.sqlite.storage import RankingType
from fbsrankings.infrastructure.sqlite.storage import SeasonTable
from fbsrankings.infrastructure.sqlite.storage import TeamRankingValueTable
from fbsrankings.infrastructure.sqlite.storage import TeamTable
from fbsrankings.query import TeamRankingBySeasonWeekQuery
from fbsrankings.query import TeamRankingBySeasonWeekResult
from fbsrankings.query import TeamRankingValueBySeasonWeekResult


SqliteParam = Union[None, int, float, str, bytes]


class TeamRankingBySeasonWeekQueryHandler(object):
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self._ranking_table = RankingTable().table
        self._value_table = TeamRankingValueTable().table
        self._season_table = SeasonTable().table
        self._team_table = TeamTable().table

    def __call__(
        self, query: TeamRankingBySeasonWeekQuery,
    ) -> Optional[TeamRankingBySeasonWeekResult]:
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
            RankingType.TEAM.name,
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
            cursor.execute(
                Query.from_(self._value_table)
                .select(
                    self._value_table.TeamID,
                    self._team_table.Name,
                    self._value_table.Ord,
                    self._value_table.Rank,
                    self._value_table.Value,
                )
                .inner_join(self._team_table)
                .on(self._team_table.UUID == self._value_table.TeamID)
                .where(self._value_table.RankingID == Parameter("?"))
                .get_sql(),
                [row[0]],
            )
            values = [
                TeamRankingValueBySeasonWeekResult(
                    UUID(value[0]), value[1], value[2], value[3], value[4],
                )
                for value in cursor.fetchall()
            ]

        cursor.close()

        if row is not None:
            return TeamRankingBySeasonWeekResult(
                UUID(row[0]), row[1], UUID(row[2]), row[3], row[4], values,
            )
        else:
            return None
