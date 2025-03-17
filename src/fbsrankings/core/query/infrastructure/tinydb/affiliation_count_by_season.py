from typing import Optional

from tinydb import Query

from communication.bus import EventBus
from fbsrankings.messages.enums import Subdivision
from fbsrankings.messages.event import AffiliationCreatedEvent
from fbsrankings.messages.query import AffiliationCountBySeasonQuery
from fbsrankings.messages.query import AffiliationCountBySeasonResult
from fbsrankings.storage.tinydb import Storage


class AffiliationCountBySeasonQueryProjection:
    def __init__(self, storage: Storage, event_bus: EventBus) -> None:
        self._connection = storage.connection
        self._event_bus = event_bus

        self._event_bus.register_handler(AffiliationCreatedEvent, self.project)

    def close(self) -> None:
        self._event_bus.unregister_handler(AffiliationCreatedEvent, self.project)

    def project(self, event: AffiliationCreatedEvent) -> None:
        table = self._connection.table("affiliation_count_by_season")

        existing = table.get(Query().season_id == event.season_id)
        if isinstance(existing, list):
            existing = existing[0]
        if existing is not None:
            if event.subdivision == Subdivision.SUBDIVISION_FBS:
                table.update(
                    {"fbs_count": existing["fbs_count"] + 1},
                    doc_ids=[existing.doc_id],
                )
            elif event.subdivision == Subdivision.SUBDIVISION_FCS:
                table.update(
                    {"fcs_count": existing["fcs_count"] + 1},
                    doc_ids=[existing.doc_id],
                )
        else:
            if event.subdivision == Subdivision.SUBDIVISION_FBS:
                table.insert(
                    {
                        "season_id": event.season_id,
                        "fbs_count": 1,
                        "fcs_count": 0,
                    },
                )
            elif event.subdivision == Subdivision.SUBDIVISION_FCS:
                table.insert(
                    {
                        "season_id": event.season_id,
                        "fbs_count": 0,
                        "fcs_count": 1,
                    },
                )


class AffiliationCountBySeasonQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._connection = storage.connection

    def __call__(
        self,
        query: AffiliationCountBySeasonQuery,
    ) -> Optional[AffiliationCountBySeasonResult]:
        table = self._connection.table("affiliation_count_by_season")

        item = table.get(Query().season_id == query.season_id)
        if isinstance(item, list):
            item = item[0]

        return (
            AffiliationCountBySeasonResult(
                season_id=item["season_id"],
                fbs_count=item["fbs_count"],
                fcs_count=item["fcs_count"],
            )
            if item is not None
            else None
        )
