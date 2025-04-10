from typing import Callable
from typing import Optional
from typing import Protocol
from typing import TypeVar


class Event(Protocol):
    event_id: str


E = TypeVar("E", bound=Event, contravariant=True)


EventHandler = Callable[[E], None]


class EventTopicMapper(Protocol):
    def get(self, key: type[E]) -> Optional[str]:
        raise NotImplementedError
