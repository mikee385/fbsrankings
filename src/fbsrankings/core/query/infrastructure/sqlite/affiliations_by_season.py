import sqlite3

from fbsrankings.messages.query import AffiliationBySeasonResult
from fbsrankings.messages.query import AffiliationsBySeasonQuery
from fbsrankings.messages.query import AffiliationsBySeasonResult
from fbsrankings.storage.sqlite import AffiliationTable
from fbsrankings.storage.sqlite import SeasonTable
from fbsrankings.storage.sqlite import TeamTable


class AffiliationsBySeasonQueryHandler:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self._season_table = SeasonTable().table
        self._team_table = TeamTable().table
        self._affiliation_table = AffiliationTable().table

    def __call__(self, query: AffiliationsBySeasonQuery) -> AffiliationsBySeasonResult:
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT "
            f"{self._affiliation_table}.UUID, "
            f"{self._affiliation_table}.SeasonID, "
            f"{self._season_table}.Year, "
            f"{self._affiliation_table}.TeamID, "
            f"{self._team_table}.Name, "
            f"{self._affiliation_table}.Subdivision "
            f"FROM {self._affiliation_table} "
            f"JOIN {self._season_table} "
            f"ON {self._season_table}.UUID = {self._affiliation_table}.SeasonID "
            f"JOIN {self._team_table} "
            f"ON {self._team_table}.UUID = {self._affiliation_table}.TeamID "
            f"WHERE {self._affiliation_table}.SeasonID = ?;",
            [query.season_id],
        )
        items = [
            AffiliationBySeasonResult(
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
            )
            for row in cursor.fetchall()
        ]
        cursor.close()

        return AffiliationsBySeasonResult(items)
