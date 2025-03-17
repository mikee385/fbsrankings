from tinydb import Query

from communication.bus import EventBus
from fbsrankings.messages.event import AffiliationCreatedEvent
from fbsrankings.messages.query import AffiliationBySeasonResult
from fbsrankings.messages.query import AffiliationsBySeasonQuery
from fbsrankings.messages.query import AffiliationsBySeasonResult
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

        existing_season = self._storage.cache_season_by_id.get(event.season_id)
        if existing_season is None:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Season {event.season_id} was not found for affiliation "
                f"{event.affiliation_id}",
            )

        existing_team = self._storage.cache_team_by_id.get(event.team_id)
        if existing_team is None:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Team {event.team_id} was not found for affiliation "
                f"{event.affiliation_id}",
            )

        existing = table.get(
            (Query().season_id == event.season_id) & (Query().team_id == event.team_id),
        )
        if isinstance(existing, list):
            existing = existing[0]
        if existing is None:
            table.insert(
                {
                    "id_": event.affiliation_id,
                    "season_id": event.season_id,
                    "year": existing_season["year"],
                    "team_id": event.team_id,
                    "team_name": existing_team["name"],
                    "subdivision": event.subdivision,
                },
            )

        elif existing["id_"] != event.affiliation_id:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"ID for affiliation does not match: "
                f"{existing['id_']} vs. {event.affiliation_id}",
            )


class AffiliationsBySeasonQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._connection = storage.connection

    def __call__(self, query: AffiliationsBySeasonQuery) -> AffiliationsBySeasonResult:
        table = self._connection.table("affiliations")

        items = [
            AffiliationBySeasonResult(
                affiliation_id=item["id_"],
                season_id=item["season_id"],
                year=item["year"],
                team_id=item["team_id"],
                team_name=item["team_name"],
                subdivision=item["subdivision"],
            )
            for item in table.search(Query().season_id == query.season_id)
        ]

        return AffiliationsBySeasonResult(affiliations=items)
