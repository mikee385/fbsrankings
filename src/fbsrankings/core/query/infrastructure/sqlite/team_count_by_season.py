import sqlite3

from fbsrankings.messages.query import TeamCountBySeasonQuery
from fbsrankings.messages.query import TeamCountBySeasonResult
from fbsrankings.storage.sqlite import AffiliationTable


class TeamCountBySeasonQueryHandler:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self._table = AffiliationTable().table

    def __call__(self, query: TeamCountBySeasonQuery) -> TeamCountBySeasonResult:
        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT COUNT(*) FROM {self._table} WHERE SeasonID = ?;",
            [query.season_id],
        )
        row = cursor.fetchone()
        cursor.close()

        return TeamCountBySeasonResult(
            query_id=query.query_id,
            season_id=query.season_id,
            count=row[0],
        )
