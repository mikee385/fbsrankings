from uuid import UUID

from fbsrankings.common import Event


class TeamCreatedEvent(Event):
    def __init__(self, id_: UUID, name: str) -> None:
        self.id_ = id_
        self.name = name
