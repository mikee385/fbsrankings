from uuid import UUID

from tinydb.table import Document

from fbsrankings.common import EventBus
from fbsrankings.core.command import SeasonCreatedEvent
from fbsrankings.core.query.query.seasons import SeasonResult
from fbsrankings.core.query.query.seasons import SeasonsQuery
from fbsrankings.core.query.query.seasons import SeasonsResult
from fbsrankings.storage.tinydb import Storage


class SeasonsQueryProjection:
    def __init__(self, storage: Storage, event_bus: EventBus) -> None:
        self._storage = storage
        self._event_bus = event_bus

        self._event_bus.register_handler(SeasonCreatedEvent, self.project)

    def close(self) -> None:
        self._event_bus.unregister_handler(SeasonCreatedEvent, self.project)

    def project(self, event: SeasonCreatedEvent) -> None:
        item = {"id_": str(event.id_), "year": event.year}

        existing_by_id = self._storage.cache_season_by_id.get(str(event.id_))
        if existing_by_id is not None and existing_by_id["year"] != item["year"]:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Year for season {event.id_} does not match: "
                f"{existing_by_id['year']} vs. {item['year']}",
            )

        existing_by_year = self._storage.cache_season_by_year.get(event.year)
        if existing_by_year is not None and existing_by_year["id_"] != item["id_"]:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"ID for season {event.year} does not match: "
                f"{existing_by_year['id_']} vs. {item['id_']}",
            )

        doc_id = self._storage.connection.table("seasons").insert(item)
        document = Document(item, doc_id)
        self._storage.cache_season_by_id[str(event.id_)] = document
        self._storage.cache_season_by_year[event.year] = document


class SeasonsQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: SeasonsQuery) -> SeasonsResult:
        return SeasonsResult(
            [
                SeasonResult(UUID(item["id_"]), item["year"])
                for item in self._storage.cache_season_by_id.values()
            ],
        )
