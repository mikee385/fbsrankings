from abc import ABCMeta
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Type
from typing import TypeVar


class Event(metaclass=ABCMeta):  # noqa: B024
    pass


E = TypeVar("E", bound=Event, contravariant=True)


EventHandler = Callable[[E], None]


class EventBus:
    def __init__(self) -> None:
        self._handlers: Dict[Type[Event], List[EventHandler[Any]]] = {}

    def register_handler(self, type_: Type[E], handler: EventHandler[E]) -> None:
        existing = self._handlers.get(type_)
        if existing is not None:
            existing.append(handler)
        else:
            self._handlers[type_] = [handler]

    def publish(self, event: E) -> None:
        handlers = self._handlers.get(type(event))
        if handlers is not None:
            for handler in handlers:
                handler(event)


class EventRecorder(EventBus):
    def __init__(self, bus: EventBus) -> None:
        super().__init__()

        self._bus = bus
        self.events: List[Event] = []

    def register_handler(self, type_: Type[E], handler: EventHandler[E]) -> None:
        self._bus.register_handler(type_, handler)

    def publish(self, event: E) -> None:
        self.events.append(event)
        self._bus.publish(event)

    def clear(self) -> None:
        self.events = []
