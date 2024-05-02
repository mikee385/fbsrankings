from uuid import UUID

from tinydb import Query

from fbsrankings.common import EventBus
from fbsrankings.core.command import AffiliationCreatedEvent
from fbsrankings.core.query.query.affiliations_by_season import (
    AffiliationBySeasonResult,
)
from fbsrankings.core.query.query.affiliations_by_season import (
    AffiliationsBySeasonQuery,
)
from fbsrankings.core.query.query.affiliations_by_season import (
    AffiliationsBySeasonResult,
)
from fbsrankings.storage.tinydb import Storage


class AffiliationsBySeasonQueryProjection:
    def __init__(self, storage: Storage, event_bus: EventBus) -> None:
        self._storage = storage
        self._event_bus = event_bus

        self._event_bus.register_handler(AffiliationCreatedEvent, self.project)

    def close(self) -> None:
        self._event_bus.unregister_handler(AffiliationCreatedEvent, self.project)

    def project(self, event: AffiliationCreatedEvent) -> None:
        table = self._storage.connection.table("affiliations")

        existing_season = self._storage.cache_season_by_id.get(str(event.season_id))
        if existing_season is None:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Season {event.season_id} was not found for affiliation {event.id_}",
            )

        existing_team = self._storage.cache_team_by_id.get(str(event.team_id))
        if existing_team is None:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Team {event.team_id} was not found for affiliation {event.id_}",
            )

        existing = table.get(
            (Query().season_id == str(event.season_id))
            & (Query().team_id == str(event.team_id)),
        )
        if isinstance(existing, list):
            existing = existing[0]
        if existing is None:
            table.insert(
                {
                    "id_": str(event.id_),
                    "season_id": str(event.season_id),
                    "year": existing_season["year"],
                    "team_id": str(event.team_id),
                    "team_name": existing_team["name"],
                    "subdivision": event.subdivision,
                },
            )

        elif existing["id_"] != str(event.id_):
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"ID for affiliation does not match: "
                f"{existing['id_']} vs. {event.id_}",
            )


class AffiliationsBySeasonQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._connection = storage.connection

    def __call__(self, query: AffiliationsBySeasonQuery) -> AffiliationsBySeasonResult:
        table = self._connection.table("affiliations")

        items = [
            AffiliationBySeasonResult(
                UUID(item["id_"]),
                UUID(item["season_id"]),
                item["year"],
                UUID(item["team_id"]),
                item["team_name"],
                item["subdivision"],
            )
            for item in table.search(Query().season_id == str(query.season_id))
        ]

        return AffiliationsBySeasonResult(items)
