from fbsrankings.messages.query import TeamByIDQuery
from fbsrankings.messages.query import TeamByIDResult
from fbsrankings.messages.query import TeamByIDValue
from fbsrankings.storage.tinydb import Storage


class TeamByIDQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: TeamByIDQuery) -> TeamByIDResult:
        item = self._storage.cache_team_by_id.get(query.team_id)

        return (
            TeamByIDResult(team=TeamByIDValue(team_id=item["id_"], name=item["name"]))
            if item is not None
            else TeamByIDResult(team=None)
        )
