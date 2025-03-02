from typing import Optional
from uuid import UUID

from tinydb import Query

from communication.bus import EventBus
from fbsrankings.messages.event import TeamRankingCalculatedEvent
from fbsrankings.messages.query import TeamRankingBySeasonWeekQuery
from fbsrankings.messages.query import TeamRankingBySeasonWeekResult
from fbsrankings.messages.query import TeamRankingValueBySeasonWeekResult
from fbsrankings.storage.tinydb import Storage


class TeamRankingBySeasonWeekQueryProjection:
    def __init__(self, storage: Storage, event_bus: EventBus) -> None:
        self._storage = storage
        self._event_bus = event_bus

        self._event_bus.register_handler(TeamRankingCalculatedEvent, self.project)

    def close(self) -> None:
        self._event_bus.unregister_handler(TeamRankingCalculatedEvent, self.project)

    def project(self, event: TeamRankingCalculatedEvent) -> None:
        table = self._storage.connection.table("team_ranking_by_season_week")

        existing_season = self._storage.cache_season_by_id.get(str(event.season_id))
        if existing_season is None:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Season {event.season_id} was not found",
            )

        values = []
        for value in event.values:
            existing_team = self._storage.cache_team_by_id.get(str(value.id_))
            if existing_team is None:
                raise RuntimeError(
                    "Query database is out of sync with master database. "
                    f"Team {value.id_} was not found for team ranking {event.id_}",
                )
            values.append(
                {
                    "id_": str(value.id_),
                    "name": existing_team["name"],
                    "order": value.order,
                    "rank": value.rank,
                    "value": value.value,
                },
            )

        existing = table.get(
            (Query().name == event.name)
            & (Query().season_id == str(event.season_id))
            & (Query().week == event.week),
        )
        if isinstance(existing, list):
            existing = existing[0]
        if existing is None:
            table.insert(
                {
                    "id_": str(event.id_),
                    "name": event.name,
                    "season_id": str(event.season_id),
                    "year": existing_season["year"],
                    "week": event.week,
                    "values": values,
                },
            )

        elif existing["id_"] != str(event.id_):
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"ID for team ranking does not match: "
                f"{existing['id_']} vs. {event.id_}",
            )


class TeamRankingBySeasonWeekQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._connection = storage.connection

    def __call__(
        self,
        query: TeamRankingBySeasonWeekQuery,
    ) -> Optional[TeamRankingBySeasonWeekResult]:
        table = self._connection.table("team_ranking_by_season_week")

        item = table.get(
            (Query().name == query.name)
            & (Query().season_id == str(query.season_id))
            & (Query().week == query.week),
        )
        if isinstance(item, list):
            item = item[0]
        return (
            TeamRankingBySeasonWeekResult(
                UUID(item["id_"]),
                item["name"],
                UUID(item["season_id"]),
                item["year"],
                item["week"],
                [
                    TeamRankingValueBySeasonWeekResult(
                        UUID(value["id_"]),
                        value["name"],
                        value["order"],
                        value["rank"],
                        value["value"],
                    )
                    for value in item["values"]
                ],
            )
            if item is not None
            else None
        )
