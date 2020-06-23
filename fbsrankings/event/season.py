from uuid import UUID

from fbsrankings.common import Event


class SeasonCreatedEvent(Event):
    def __init__(self, ID: UUID, year: int) -> None:
        self.ID = ID
        self.year = year
