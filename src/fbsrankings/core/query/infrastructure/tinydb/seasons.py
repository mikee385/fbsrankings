from uuid import UUID

from tinydb import Query

from fbsrankings.common import EventBus
from fbsrankings.core.command import SeasonCreatedEvent
from fbsrankings.core.query.query.seasons import SeasonResult
from fbsrankings.core.query.query.seasons import SeasonsQuery
from fbsrankings.core.query.query.seasons import SeasonsResult
from fbsrankings.storage.tinydb import Storage


class SeasonsQueryProjection:
    def __init__(self, storage: Storage, event_bus: EventBus) -> None:
        self._connection = storage.connection
        self._event_bus = event_bus

        self._event_bus.register_handler(SeasonCreatedEvent, self.project)

    def close(self) -> None:
        self._event_bus.unregister_handler(SeasonCreatedEvent, self.project)

    def project(self, event: SeasonCreatedEvent) -> None:
        table = self._connection.table("seasons")

        existing = table.get(Query().year == event.year)
        if existing is None:
            table.insert({"id_": str(event.id_), "year": event.year})

        elif existing["id_"] != str(event.id_):
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"ID for season {event.year} does not match: "
                f"{existing['id_']} vs. {event.id_}",
            )


class SeasonsQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._connection = storage.connection

    def __call__(self, query: SeasonsQuery) -> SeasonsResult:
        table = self._connection.table("seasons")

        items = [SeasonResult(UUID(item["id_"]), item["year"]) for item in table.all()]

        return SeasonsResult(items)
