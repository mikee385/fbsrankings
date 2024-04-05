from typing import Optional
from uuid import UUID

from tinydb import Query

from fbsrankings.common import EventBus
from fbsrankings.core.command import GameCreatedEvent
from fbsrankings.core.query.query.postseason_game_count_by_season import (
    PostseasonGameCountBySeasonQuery,
)
from fbsrankings.core.query.query.postseason_game_count_by_season import (
    PostseasonGameCountBySeasonResult,
)
from fbsrankings.enum import SeasonSection
from fbsrankings.storage.tinydb import Storage


class PostseasonGameCountBySeasonQueryProjection:
    def __init__(self, storage: Storage, event_bus: EventBus) -> None:
        self._connection = storage.connection
        self._event_bus = event_bus

        self._event_bus.register_handler(GameCreatedEvent, self.project)

    def close(self) -> None:
        self._event_bus.unregister_handler(GameCreatedEvent, self.project)

    def project(self, event: GameCreatedEvent) -> None:
        if event.season_section == SeasonSection.POSTSEASON.name:
            table = self._connection.table("postseason_game_count_by_season")

            existing = table.get(Query().season_id == str(event.season_id))
            if existing is not None:
                table.update(
                    {"count": existing["count"] + 1},
                    doc_ids=[existing.doc_id],
                )
            else:
                table.insert(
                    {
                        "season_id": str(event.season_id),
                        "count": 1,
                    },
                )


class PostseasonGameCountBySeasonQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._connection = storage.connection

    def __call__(
        self,
        query: PostseasonGameCountBySeasonQuery,
    ) -> Optional[PostseasonGameCountBySeasonResult]:
        table = self._connection.table("postseason_game_count_by_season")

        item = table.get(Query().season_id == str(query.season_id))

        return (
            PostseasonGameCountBySeasonResult(UUID(item["season_id"]), item["count"])
            if item is not None
            else None
        )
