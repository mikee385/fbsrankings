from uuid import UUID

from fbsrankings.common import Event


class SeasonCreatedEvent(Event):
    def __init__(self, id: UUID, year: int) -> None:
        self.id = id
        self.year = year
