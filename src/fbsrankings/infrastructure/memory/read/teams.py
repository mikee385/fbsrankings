from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.query import TeamResult
from fbsrankings.query import TeamsQuery
from fbsrankings.query import TeamsResult


class TeamsQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: TeamsQuery) -> TeamsResult:
        return TeamsResult(
            [TeamResult(item.id_, item.name) for item in self._storage.team.all_()],
        )
