import sqlite3
from uuid import UUID

from pypika import Parameter
from pypika import Query

from fbsrankings.shared.query import AffiliationBySeasonResult
from fbsrankings.shared.query import AffiliationsBySeasonQuery
from fbsrankings.shared.query import AffiliationsBySeasonResult
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
            Query.from_(self._affiliation_table)
            .select(
                self._affiliation_table.UUID,
                self._affiliation_table.SeasonID,
                self._season_table.Year,
                self._affiliation_table.TeamID,
                self._team_table.Name,
                self._affiliation_table.Subdivision,
            )
            .inner_join(self._season_table)
            .on(self._season_table.UUID == self._affiliation_table.SeasonID)
            .inner_join(self._team_table)
            .on(self._team_table.UUID == self._affiliation_table.TeamID)
            .where(self._affiliation_table.SeasonID == Parameter("?"))
            .get_sql(),
            [str(query.season_id)],
        )
        items = [
            AffiliationBySeasonResult(
                UUID(row[0]),
                UUID(row[1]),
                row[2],
                UUID(row[3]),
                row[4],
                row[5],
            )
            for row in cursor.fetchall()
        ]
        cursor.close()

        return AffiliationsBySeasonResult(items)
