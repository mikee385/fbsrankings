from typing import Optional

from tinydb import Query

from communication.bus import EventBus
from fbsrankings.messages.event import TeamRecordCalculatedEvent
from fbsrankings.messages.query import TeamRecordBySeasonWeekQuery
from fbsrankings.messages.query import TeamRecordBySeasonWeekResult
from fbsrankings.messages.query import TeamRecordValueBySeasonWeekResult
from fbsrankings.storage.tinydb import Storage


class TeamRecordBySeasonWeekQueryProjection:
    def __init__(self, storage: Storage, event_bus: EventBus) -> None:
        self._storage = storage
        self._event_bus = event_bus

        self._event_bus.register_handler(TeamRecordCalculatedEvent, self.project)

    def close(self) -> None:
        self._event_bus.unregister_handler(TeamRecordCalculatedEvent, self.project)

    def project(self, event: TeamRecordCalculatedEvent) -> None:
        table = self._storage.connection.table("team_record_by_season_week")

        existing_season = self._storage.cache_season_by_id.get(event.season_id)
        if existing_season is None:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Season {event.season_id} was not found",
            )

        values = []
        for value in event.values:
            existing_team = self._storage.cache_team_by_id.get(value.team_id)
            if existing_team is None:
                raise RuntimeError(
                    "Query database is out of sync with master database. "
                    f"Team {value.team_id} was not found for team record {event.record_id}",
                )
            values.append(
                {
                    "id_": value.team_id,
                    "name": existing_team["name"],
                    "wins": value.wins,
                    "losses": value.losses,
                },
            )

        existing = table.get(
            (Query().season_id == event.season_id) & (Query().week == event.week),
        )
        if isinstance(existing, list):
            existing = existing[0]
        if existing is None:
            table.insert(
                {
                    "id_": event.record_id,
                    "season_id": event.season_id,
                    "year": existing_season["year"],
                    "week": event.week,
                    "values": values,
                },
            )

        elif existing["id_"] != event.record_id:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"ID for team record does not match: "
                f"{existing['id_']} vs. {event.record_id}",
            )


class TeamRecordBySeasonWeekQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._connection = storage.connection

    def __call__(
        self,
        query: TeamRecordBySeasonWeekQuery,
    ) -> Optional[TeamRecordBySeasonWeekResult]:
        table = self._connection.table("team_record_by_season_week")

        item = table.get(
            (Query().season_id == query.season_id) & (Query().week == query.week),
        )
        if isinstance(item, list):
            item = item[0]
        return (
            TeamRecordBySeasonWeekResult(
                item["id_"],
                item["season_id"],
                item["year"],
                item["week"],
                [
                    TeamRecordValueBySeasonWeekResult(
                        value["id_"],
                        value["name"],
                        value["wins"],
                        value["losses"],
                    )
                    for value in item["values"]
                ],
            )
            if item is not None
            else None
        )
