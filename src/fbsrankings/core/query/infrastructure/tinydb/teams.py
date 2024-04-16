from uuid import UUID

from tinydb import Query

from fbsrankings.common import EventBus
from fbsrankings.core.command import TeamCreatedEvent
from fbsrankings.core.query.query.teams import TeamResult
from fbsrankings.core.query.query.teams import TeamsQuery
from fbsrankings.core.query.query.teams import TeamsResult
from fbsrankings.storage.tinydb import Storage


class TeamsQueryProjection:
    def __init__(self, storage: Storage, event_bus: EventBus) -> None:
        self._connection = storage.connection
        self._event_bus = event_bus

        self._event_bus.register_handler(TeamCreatedEvent, self.project)

    def close(self) -> None:
        self._event_bus.unregister_handler(TeamCreatedEvent, self.project)

    def project(self, event: TeamCreatedEvent) -> None:
        table = self._connection.table("teams")

        existing = table.get(Query().name == event.name)
        if isinstance(existing, list):
            existing = existing[0]
        if existing is None:
            table.insert({"id_": str(event.id_), "name": event.name})

        elif existing["id_"] != str(event.id_):
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"ID for team {event.name} does not match: "
                f"{existing['id_']} vs. {event.id_}",
            )


class TeamsQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._connection = storage.connection

    def __call__(self, query: TeamsQuery) -> TeamsResult:
        table = self._connection.table("teams")

        items = [TeamResult(UUID(item["id_"]), item["name"]) for item in table.all()]

        return TeamsResult(items)
