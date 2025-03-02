from typing import cast
from typing import Optional
from uuid import UUID

from tinydb import Query

from communication.bus import EventBus
from fbsrankings.messages.event import GameCanceledEvent
from fbsrankings.messages.event import GameCompletedEvent
from fbsrankings.messages.event import GameCreatedEvent
from fbsrankings.messages.event import GameRescheduledEvent
from fbsrankings.messages.query import LatestSeasonWeekQuery
from fbsrankings.messages.query import LatestSeasonWeekResult
from fbsrankings.storage.tinydb import Storage


class LatestSeasonWeekQueryProjection:
    def __init__(self, storage: Storage, event_bus: EventBus) -> None:
        self._storage = storage
        self._event_bus = event_bus

        self._event_bus.register_handler(GameCreatedEvent, self.project_created)
        self._event_bus.register_handler(GameCanceledEvent, self.project_canceled)
        self._event_bus.register_handler(GameCompletedEvent, self.project_completed)
        self._event_bus.register_handler(GameRescheduledEvent, self.project_rescheduled)

    def close(self) -> None:
        self._event_bus.unregister_handler(GameCreatedEvent, self.project_created)
        self._event_bus.unregister_handler(GameCanceledEvent, self.project_canceled)
        self._event_bus.unregister_handler(GameCompletedEvent, self.project_completed)
        self._event_bus.unregister_handler(
            GameRescheduledEvent,
            self.project_rescheduled,
        )

    def project_created(self, event: GameCreatedEvent) -> None:
        existing_season = self._storage.cache_season_by_id.get(str(event.season_id))
        if existing_season is None:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Season {event.season_id} was not found",
            )

        season_count_table = self._storage.connection.table("game_status_season_count")
        season_count = season_count_table.get(Query().season_id == str(event.season_id))
        if isinstance(season_count, list):
            season_count = season_count[0]
        if season_count is not None:
            season_count_table.update(
                {"scheduled_count": season_count["scheduled_count"] + 1},
                doc_ids=[season_count.doc_id],
            )
        else:
            season_count_table.insert(
                {
                    "season_id": str(event.season_id),
                    "year": existing_season["year"],
                    "scheduled_count": 1,
                    "completed_count": 0,
                    "canceled_count": 0,
                },
            )

        week_table = self._storage.connection.table("game_status_week_count")
        week_count = week_table.get(
            (Query().season_id == str(event.season_id)) & (Query().week == event.week),
        )
        if isinstance(week_count, list):
            week_count = week_count[0]
        if week_count is not None:
            week_table.update(
                {"scheduled_count": week_count["scheduled_count"] + 1},
                doc_ids=[week_count.doc_id],
            )
        else:
            week_table.insert(
                {
                    "season_id": str(event.season_id),
                    "year": existing_season["year"],
                    "week": event.week,
                    "scheduled_count": 1,
                    "completed_count": 0,
                    "canceled_count": 0,
                },
            )

        self._storage.connection.drop_table("latest_season_week")

    def project_canceled(self, event: GameCanceledEvent) -> None:
        existing_season = self._storage.cache_season_by_id.get(str(event.season_id))
        if existing_season is None:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Season {event.season_id} was not found",
            )

        season_count_table = self._storage.connection.table("game_status_season_count")
        season_count = season_count_table.get(Query().season_id == str(event.season_id))
        if isinstance(season_count, list):
            season_count = season_count[0]
        if season_count is not None:
            season_count_table.update(
                {"canceled_count": season_count["canceled_count"] + 1},
                doc_ids=[season_count.doc_id],
            )
        else:
            season_count_table.insert(
                {
                    "season_id": str(event.season_id),
                    "year": existing_season["year"],
                    "scheduled_count": 0,
                    "completed_count": 0,
                    "canceled_count": 1,
                },
            )

        week_table = self._storage.connection.table("game_status_week_count")
        week_count = week_table.get(
            (Query().season_id == str(event.season_id)) & (Query().week == event.week),
        )
        if isinstance(week_count, list):
            week_count = week_count[0]
        if week_count is not None:
            week_table.update(
                {"canceled_count": week_count["canceled_count"] + 1},
                doc_ids=[week_count.doc_id],
            )
        else:
            week_table.insert(
                {
                    "season_id": str(event.season_id),
                    "year": existing_season["year"],
                    "week": event.week,
                    "scheduled_count": 0,
                    "completed_count": 0,
                    "canceled_count": 1,
                },
            )

        self._storage.connection.drop_table("latest_season_week")

    def project_completed(self, event: GameCompletedEvent) -> None:
        existing_season = self._storage.cache_season_by_id.get(str(event.season_id))
        if existing_season is None:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Season {event.season_id} was not found",
            )

        season_count_table = self._storage.connection.table("game_status_season_count")
        season_count = season_count_table.get(Query().season_id == str(event.season_id))
        if isinstance(season_count, list):
            season_count = season_count[0]
        if season_count is not None:
            season_count_table.update(
                {"completed_count": season_count["completed_count"] + 1},
                doc_ids=[season_count.doc_id],
            )
        else:
            season_count_table.insert(
                {
                    "season_id": str(event.season_id),
                    "year": existing_season["year"],
                    "scheduled_count": 0,
                    "completed_count": 1,
                    "canceled_count": 0,
                },
            )

        week_count_table = self._storage.connection.table("game_status_week_count")
        week_count = week_count_table.get(
            (Query().season_id == str(event.season_id)) & (Query().week == event.week),
        )
        if isinstance(week_count, list):
            week_count = week_count[0]
        if week_count is not None:
            week_count_table.update(
                {"completed_count": week_count["completed_count"] + 1},
                doc_ids=[week_count.doc_id],
            )
        else:
            week_count_table.insert(
                {
                    "season_id": str(event.season_id),
                    "year": existing_season["year"],
                    "week": event.week,
                    "scheduled_count": 0,
                    "completed_count": 1,
                    "canceled_count": 0,
                },
            )

        self._storage.connection.drop_table("latest_season_week")

    def project_rescheduled(self, event: GameRescheduledEvent) -> None:
        existing_season = self._storage.cache_season_by_id.get(str(event.season_id))
        if existing_season is None:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Season {event.season_id} was not found",
            )

        week_count_table = self._storage.connection.table("game_status_week_count")

        old_week_count = week_count_table.get(
            (Query().season_id == str(event.season_id))
            & (Query().week == event.old_week),
        )
        if isinstance(old_week_count, list):
            old_week_count = old_week_count[0]
        if old_week_count is not None:
            week_count_table.update(
                {"scheduled_count": old_week_count["scheduled_count"] - 1},
                doc_ids=[old_week_count.doc_id],
            )

        new_week_count = week_count_table.get(
            (Query().season_id == str(event.season_id)) & (Query().week == event.week),
        )
        if isinstance(new_week_count, list):
            new_week_count = new_week_count[0]
        if new_week_count is not None:
            week_count_table.update(
                {"scheduled_count": new_week_count["scheduled_count"] + 1},
                doc_ids=[new_week_count.doc_id],
            )
        else:
            week_count_table.insert(
                {
                    "season_id": str(event.season_id),
                    "year": existing_season["year"],
                    "week": event.week,
                    "scheduled_count": 1,
                    "completed_count": 0,
                    "canceled_count": 0,
                },
            )

        self._storage.connection.drop_table("latest_season_week")


class LatestSeasonWeekQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(
        self,
        query: LatestSeasonWeekQuery,
    ) -> Optional[LatestSeasonWeekResult]:
        table = self._storage.connection.table("latest_season_week")

        items = table.all()
        if len(items) > 0:
            item = items[0]
            return LatestSeasonWeekResult(
                UUID(item["season_id"]),
                item["year"],
                item["week"],
            )

        season_count_table = self._storage.connection.table("game_status_season_count")
        season_counts = season_count_table.all()
        for season in sorted(
            season_counts,
            key=lambda s: cast(
                int,
                s["year"],
            ),
            reverse=True,
        ):
            if (
                season["scheduled_count"]
                <= season["completed_count"] + season["canceled_count"]
            ):
                table.insert(
                    {
                        "season_id": season["season_id"],
                        "year": season["year"],
                        "week": None,
                    },
                )
                return LatestSeasonWeekResult(
                    UUID(season["season_id"]),
                    season["year"],
                    None,
                )

            if season["completed_count"] > 0:
                week_table = self._storage.connection.table("game_status_week_count")
                week_counts = week_table.search(
                    Query().season_id == season["season_id"],
                )
                if len(week_counts) == 0:
                    raise RuntimeError(
                        "Query database is out of sync with master database. "
                        f"Game Status Weeks were not found for season {season['season_id']}",
                    )

                for week in sorted(
                    week_counts,
                    key=lambda w: cast(
                        int,
                        w["week"],
                    ),
                    reverse=True,
                ):
                    if (
                        week["scheduled_count"]
                        <= week["completed_count"] + week["canceled_count"]
                    ):
                        existing_season = self._storage.cache_season_by_id.get(
                            week["season_id"],
                        )
                        if existing_season is None:
                            raise RuntimeError(
                                "Query database is out of sync with master database. "
                                f"Season {week['season_id']} was not found",
                            )

                        table.insert(
                            {
                                "season_id": week["season_id"],
                                "year": existing_season["year"],
                                "week": week["week"],
                            },
                        )
                        return LatestSeasonWeekResult(
                            UUID(week["season_id"]),
                            existing_season["year"],
                            week["week"],
                        )

        return None
