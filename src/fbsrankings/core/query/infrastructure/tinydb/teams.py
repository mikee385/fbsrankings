from uuid import UUID

from tinydb.table import Document

from communication.bus import EventBus
from fbsrankings.messages.event import TeamCreatedEvent
from fbsrankings.messages.query import TeamResult
from fbsrankings.messages.query import TeamsQuery
from fbsrankings.messages.query import TeamsResult
from fbsrankings.storage.tinydb import Storage


class TeamsQueryProjection:
    def __init__(self, storage: Storage, event_bus: EventBus) -> None:
        self._storage = storage
        self._event_bus = event_bus

        self._event_bus.register_handler(TeamCreatedEvent, self.project)

    def close(self) -> None:
        self._event_bus.unregister_handler(TeamCreatedEvent, self.project)

    def project(self, event: TeamCreatedEvent) -> None:
        item = {"id_": str(event.team_id), "name": event.name}

        existing_by_id = self._storage.cache_team_by_id.get(str(event.team_id))
        if existing_by_id is not None and existing_by_id["name"] != item["name"]:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Name for team {event.team_id} does not match: "
                f"{existing_by_id['name']} vs. {item['name']}",
            )

        existing_by_name = self._storage.cache_team_by_name.get(event.name)
        if existing_by_name is not None and existing_by_name["id_"] != item["id_"]:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"ID for team {event.name} does not match: "
                f"{existing_by_name['id_']} vs. {item['id_']}",
            )

        doc_id = self._storage.connection.table("teams").insert(item)
        document = Document(item, doc_id)
        self._storage.cache_team_by_id[str(event.team_id)] = document
        self._storage.cache_team_by_name[event.name] = document


class TeamsQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: TeamsQuery) -> TeamsResult:
        return TeamsResult(
            [
                TeamResult(UUID(item["id_"]), item["name"])
                for item in self._storage.cache_team_by_id.values()
            ],
        )
