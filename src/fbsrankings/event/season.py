from uuid import UUID

from dataclasses import dataclass

from fbsrankings.common import Event


@dataclass(frozen=True)
class SeasonCreatedEvent(Event):
    id_: UUID
    year: int
