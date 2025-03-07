from typing import Callable
from typing import TypeVar
from uuid import UUID

from typing_extensions import Protocol


class Event(Protocol):
    event_id: UUID


E = TypeVar("E", bound=Event, contravariant=True)


EventHandler = Callable[[E], None]
