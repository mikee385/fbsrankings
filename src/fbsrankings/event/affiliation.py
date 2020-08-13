from uuid import UUID

from dataclasses import dataclass

from fbsrankings.common import Event


@dataclass(frozen=True)
class AffiliationCreatedEvent(Event):
    id_: UUID
    season_id: UUID
    team_id: UUID
    subdivision: str
