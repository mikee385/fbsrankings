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
        self._connection = storage.connection
        self._event_bus = event_bus

        self._event_bus.register_handler(AffiliationCreatedEvent, self.project)

    def close(self) -> None:
        self._event_bus.unregister_handler(AffiliationCreatedEvent, self.project)

    def project(self, event: AffiliationCreatedEvent) -> None:
        table = self._connection.table("affiliations")

        season_table = self._connection.table("seasons")
        existing_season = season_table.get(Query().id_ == str(event.season_id))
        if existing_season is None:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Season {event.season_id} was not found for affiliation {event.id_}",
            )

        team_table = self._connection.table("teams")
        existing_team = team_table.get(Query().id_ == str(event.team_id))
        if existing_team is None:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Home Team {event.team_id} was not found for affiliation {event.id_}",
            )

        existing = table.get(
            (Query().season_id == str(event.season_id))
            & (Query().team_id == str(event.team_id)),
        )
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
