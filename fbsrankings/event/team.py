from uuid import UUID

from fbsrankings.common import Event


class TeamCreatedEvent(Event):
    def __init__(self, id: UUID, name: str) -> None:
        self.id = id
        self.name = name
