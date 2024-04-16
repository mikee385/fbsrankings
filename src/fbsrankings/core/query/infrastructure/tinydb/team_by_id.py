from typing import Optional
from uuid import UUID

from tinydb import Query

from fbsrankings.core.query.query.team_by_id import TeamByIDQuery
from fbsrankings.core.query.query.team_by_id import TeamByIDResult
from fbsrankings.storage.tinydb import Storage


class TeamByIDQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._connection = storage.connection

    def __call__(self, query: TeamByIDQuery) -> Optional[TeamByIDResult]:
        table = self._connection.table("teams")

        item = table.get(Query().id_ == str(query.id_))
        if isinstance(item, list):
            item = item[0]

        return (
            TeamByIDResult(UUID(item["id_"]), item["name"])
            if item is not None
            else None
        )
