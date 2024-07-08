import sqlite3

from fbsrankings.shared.query import TeamCountBySeasonQuery
from fbsrankings.shared.query import TeamCountBySeasonResult
from fbsrankings.storage.sqlite import AffiliationTable


class TeamCountBySeasonQueryHandler:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self._table = AffiliationTable().table

    def __call__(self, query: TeamCountBySeasonQuery) -> TeamCountBySeasonResult:
        cursor = self._connection.cursor()
        cursor.execute(
            f"SELECT COUNT(*) FROM {self._table} WHERE SeasonID = ?;",
            [str(query.season_id)],
        )
        row = cursor.fetchone()
        cursor.close()

        return TeamCountBySeasonResult(query.season_id, row[0])
