from uuid import UUID

from tinydb.table import Document

from communication.bus import EventBus
from fbsrankings.messages.event import SeasonCreatedEvent
from fbsrankings.messages.query import SeasonResult
from fbsrankings.messages.query import SeasonsQuery
from fbsrankings.messages.query import SeasonsResult
from fbsrankings.storage.tinydb import Storage


class SeasonsQueryProjection:
    def __init__(self, storage: Storage, event_bus: EventBus) -> None:
        self._storage = storage
        self._event_bus = event_bus

        self._event_bus.register_handler(SeasonCreatedEvent, self.project)

    def close(self) -> None:
        self._event_bus.unregister_handler(SeasonCreatedEvent, self.project)

    def project(self, event: SeasonCreatedEvent) -> None:
        item = {"id_": str(event.season_id), "year": event.year}

        existing_by_id = self._storage.cache_season_by_id.get(str(event.season_id))
        if existing_by_id is not None and existing_by_id["year"] != item["year"]:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Year for season {event.season_id} does not match: "
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
        self._storage.cache_season_by_id[str(event.season_id)] = document
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
