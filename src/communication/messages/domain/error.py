from typing import Protocol

from .event import Event


class Error(Event, Protocol):
    event_id: str
    message: str


class MultipleError(Error):
    def __init__(self, event_id: str, errors: list[Error]) -> None:
        self.event_id = event_id
        self.message = (
            "Multiple errors have occurred. See the errors property for more details."
        )
        self.errors = errors
