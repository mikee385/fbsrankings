from uuid import UUID

from dataclasses import dataclass

from fbsrankings.common import Event


@dataclass(frozen=True)
class TeamCreatedEvent(Event):
    id_: UUID
    name: str
