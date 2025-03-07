from typing import Callable
from typing import TypeVar

from typing_extensions import Protocol


class Event(Protocol):
    event_id: str


E = TypeVar("E", bound=Event, contravariant=True)


EventHandler = Callable[[E], None]
