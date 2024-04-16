from typing import Optional
from uuid import UUID

from tinydb import Query

from fbsrankings.core.query.query.season_by_year import SeasonByYearQuery
from fbsrankings.core.query.query.season_by_year import SeasonByYearResult
from fbsrankings.storage.tinydb import Storage


class SeasonByYearQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._connection = storage.connection

    def __call__(self, query: SeasonByYearQuery) -> Optional[SeasonByYearResult]:
        table = self._connection.table("seasons")

        item = table.get(Query().year == query.year)
        if isinstance(item, list):
            item = item[0]

        return (
            SeasonByYearResult(UUID(item["id_"]), item["year"])
            if item is not None
            else None
        )
