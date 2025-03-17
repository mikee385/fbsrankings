from fbsrankings.messages.query import TeamResult
from fbsrankings.messages.query import TeamsQuery
from fbsrankings.messages.query import TeamsResult
from fbsrankings.storage.memory import Storage


class TeamsQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: TeamsQuery) -> TeamsResult:
        return TeamsResult(
            teams=[
                TeamResult(team_id=str(item.id_), name=item.name)
                for item in self._storage.team.all_()
            ],
        )
