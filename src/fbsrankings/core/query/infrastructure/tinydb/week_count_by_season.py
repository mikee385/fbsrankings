from typing import Optional
from uuid import UUID

from tinydb import Query

from fbsrankings.common import EventBus
from fbsrankings.core.command import GameCreatedEvent
from fbsrankings.core.query.query.week_count_by_season import WeekCountBySeasonQuery
from fbsrankings.core.query.query.week_count_by_season import WeekCountBySeasonResult
from fbsrankings.storage.tinydb import Storage


class WeekCountBySeasonQueryProjection:
    def __init__(self, storage: Storage, event_bus: EventBus) -> None:
        self._connection = storage.connection
        self._event_bus = event_bus

        self._event_bus.register_handler(GameCreatedEvent, self.project)

    def close(self) -> None:
        self._event_bus.unregister_handler(GameCreatedEvent, self.project)

    def project(self, event: GameCreatedEvent) -> None:
        table = self._connection.table("week_count_by_season")

        existing = table.get(Query().season_id == str(event.season_id))
        if existing is not None:
            if event.week > existing["count"]:
                table.update({"count": event.week}, doc_ids=[existing.doc_id])
        else:
            table.insert(
                {
                    "season_id": str(event.season_id),
                    "count": event.week,
                },
            )


class WeekCountBySeasonQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._connection = storage.connection

    def __call__(
        self,
        query: WeekCountBySeasonQuery,
    ) -> Optional[WeekCountBySeasonResult]:
        table = self._connection.table("week_count_by_season")

        item = table.get(Query().season_id == str(query.season_id))

        return (
            WeekCountBySeasonResult(UUID(item["season_id"]), item["count"])
            if item is not None
            else None
        )
