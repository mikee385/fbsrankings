from uuid import UUID

from fbsrankings.common import Event


class TeamCreatedEvent(Event):
    def __init__(self, ID: UUID, name: str) -> None:
        self.ID = ID
        self.name = name
