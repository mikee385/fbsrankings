import sqlite3
from typing import Optional
from uuid import UUID

from pypika import Case
from pypika import Order
from pypika import Parameter
from pypika import Query
from pypika.functions import Sum

from fbsrankings.shared.enums import GameStatus
from fbsrankings.shared.query import LatestSeasonWeekQuery
from fbsrankings.shared.query import LatestSeasonWeekResult
from fbsrankings.storage.sqlite import GameTable
from fbsrankings.storage.sqlite import SeasonTable


class LatestSeasonWeekQueryHandler:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self._season_table = SeasonTable().table
        self._game_table = GameTable().table

    def __call__(
        self,
        query: LatestSeasonWeekQuery,
    ) -> Optional[LatestSeasonWeekResult]:
        season_subquery = (
            Query.from_(self._game_table)
            .select(
                self._game_table.SeasonID,
                self._season_table.Year,
                Sum(
                    Case().when(self._game_table.Status == Parameter("?"), 1).else_(0),
                ).as_("GamesCompleted"),
                Sum(
                    Case().when(self._game_table.Status == Parameter("?"), 1).else_(0),
                ).as_("GamesScheduled"),
            )
            .inner_join(self._season_table)
            .on(self._season_table.UUID == self._game_table.SeasonID)
            .groupby(self._game_table.SeasonID, self._season_table.Year)
            .as_("season")
        )

        cursor = self._connection.cursor()
        cursor.execute(
            Query.from_(season_subquery)
            .select(
                season_subquery.SeasonID,
                season_subquery.Year,
                season_subquery.GamesScheduled,
            )
            .where(season_subquery.GamesCompleted > 0)
            .orderby(season_subquery.Year, order=Order.desc)
            .limit(1)
            .get_sql(),
            [GameStatus.COMPLETED.name, GameStatus.SCHEDULED.name],
        )
        row = cursor.fetchone()
        cursor.close()

        if row is None:
            return None

        season_id, year, games_scheduled = row

        if games_scheduled == 0:
            return LatestSeasonWeekResult(UUID(season_id), year, None)

        week_subquery = (
            Query.from_(self._game_table)
            .select(
                self._game_table.Week,
                Sum(
                    Case().when(self._game_table.Status == Parameter("?"), 1).else_(0),
                ).as_("GamesCompleted"),
                Sum(
                    Case().when(self._game_table.Status == Parameter("?"), 1).else_(0),
                ).as_("GamesScheduled"),
            )
            .where(self._game_table.SeasonID == Parameter("?"))
            .groupby(self._game_table.Week)
            .as_("week")
        )

        cursor = self._connection.cursor()
        cursor.execute(
            Query.from_(week_subquery)
            .select(week_subquery.Week)
            .where(
                (week_subquery.GamesCompleted > 0)
                & (week_subquery.GamesScheduled == 0),
            )
            .orderby(week_subquery.Week, order=Order.desc)
            .limit(1)
            .get_sql(),
            [GameStatus.COMPLETED.name, GameStatus.SCHEDULED.name, season_id],
        )
        row = cursor.fetchone()
        cursor.close()

        if row:
            return LatestSeasonWeekResult(UUID(season_id), year, row[0])

        return None
