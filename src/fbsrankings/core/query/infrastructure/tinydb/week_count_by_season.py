from tinydb import Query

from communication.bus import EventBus
from fbsrankings.messages.event import GameCreatedEvent
from fbsrankings.messages.query import WeekCountBySeasonQuery
from fbsrankings.messages.query import WeekCountBySeasonResult
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

        existing = table.get(Query().season_id == event.season_id)
        if isinstance(existing, list):
            existing = existing[0]
        if existing is not None:
            if event.week > existing["count"]:
                table.update({"count": event.week}, doc_ids=[existing.doc_id])
        else:
            table.insert(
                {
                    "season_id": event.season_id,
                    "count": event.week,
                },
            )


class WeekCountBySeasonQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._connection = storage.connection

    def __call__(
        self,
        query: WeekCountBySeasonQuery,
    ) -> WeekCountBySeasonResult:
        table = self._connection.table("week_count_by_season")

        item = table.get(Query().season_id == query.season_id)
        if isinstance(item, list):
            item = item[0]

        if item is not None:
            return WeekCountBySeasonResult(
                season_id=item["season_id"],
                count=item["count"],
            )

        return WeekCountBySeasonResult(season_id=query.season_id, count=0)
