from typing import Optional
from uuid import UUID

from tinydb import Query

from fbsrankings.common import EventBus
from fbsrankings.core.command import GameCreatedEvent
from fbsrankings.core.query.query.game_count_by_season import GameCountBySeasonQuery
from fbsrankings.core.query.query.game_count_by_season import GameCountBySeasonResult
from fbsrankings.storage.tinydb import Storage


class GameCountBySeasonQueryProjection:
    def __init__(self, storage: Storage, event_bus: EventBus) -> None:
        self._connection = storage.connection
        self._event_bus = event_bus

        self._event_bus.register_handler(GameCreatedEvent, self.project)

    def close(self) -> None:
        self._event_bus.unregister_handler(GameCreatedEvent, self.project)

    def project(self, event: GameCreatedEvent) -> None:
        table = self._connection.table("game_count_by_season")

        existing = table.get(Query().season_id == str(event.season_id))
        if isinstance(existing, list):
            existing = existing[0]
        if existing is not None:
            table.update({"count": existing["count"] + 1}, doc_ids=[existing.doc_id])
        else:
            table.insert(
                {
                    "season_id": str(event.season_id),
                    "count": 1,
                },
            )


class GameCountBySeasonQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._connection = storage.connection

    def __call__(
        self,
        query: GameCountBySeasonQuery,
    ) -> Optional[GameCountBySeasonResult]:
        table = self._connection.table("game_count_by_season")

        item = table.get(Query().season_id == str(query.season_id))
        if isinstance(item, list):
            item = item[0]

        return (
            GameCountBySeasonResult(UUID(item["season_id"]), item["count"])
            if item is not None
            else None
        )
