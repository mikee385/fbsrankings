from typing import Optional

from tinydb import Query

from communication.bus import EventBus
from fbsrankings.messages.event import AffiliationCreatedEvent
from fbsrankings.messages.query import TeamCountBySeasonQuery
from fbsrankings.messages.query import TeamCountBySeasonResult
from fbsrankings.storage.tinydb import Storage


class TeamCountBySeasonQueryProjection:
    def __init__(self, storage: Storage, event_bus: EventBus) -> None:
        self._connection = storage.connection
        self._event_bus = event_bus

        self._event_bus.register_handler(AffiliationCreatedEvent, self.project)

    def close(self) -> None:
        self._event_bus.unregister_handler(AffiliationCreatedEvent, self.project)

    def project(self, event: AffiliationCreatedEvent) -> None:
        table = self._connection.table("team_count_by_season")

        existing = table.get(Query().season_id == event.season_id)
        if isinstance(existing, list):
            existing = existing[0]
        if existing is not None:
            table.update({"count": existing["count"] + 1}, doc_ids=[existing.doc_id])
        else:
            table.insert(
                {
                    "season_id": event.season_id,
                    "count": 1,
                },
            )


class TeamCountBySeasonQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._connection = storage.connection

    def __call__(
        self,
        query: TeamCountBySeasonQuery,
    ) -> Optional[TeamCountBySeasonResult]:
        table = self._connection.table("team_count_by_season")

        item = table.get(Query().season_id == query.season_id)
        if isinstance(item, list):
            item = item[0]

        return (
            TeamCountBySeasonResult(season_id=item["season_id"], count=item["count"])
            if item is not None
            else None
        )
