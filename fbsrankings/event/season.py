from uuid import UUID

from fbsrankings.common import Event


class SeasonCreatedEvent(Event):
    def __init__(self, id_: UUID, year: int) -> None:
        self.id_ = id_
        self.year = year
