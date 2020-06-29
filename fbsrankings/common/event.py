from abc import ABCMeta
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Type
from typing import TypeVar


class Event(metaclass=ABCMeta):
    pass


E = TypeVar("E", bound=Event, contravariant=True)


EventHandler = Callable[[E], None]


class EventBus(object):
    def __init__(self) -> None:
        self._handlers: Dict[Type[Event], List[EventHandler[Any]]] = {}

    def register_handler(self, type: Type[E], handler: EventHandler[E]) -> None:
        existing = self._handlers.get(type)
        if existing is not None:
            existing.append(handler)
        else:
            self._handlers[type] = [handler]

    def publish(self, event: E) -> None:
        handlers = self._handlers.get(type(event))
        if handlers is not None:
            for handler in handlers:
                handler(event)


class EventRecorder(EventBus):
    def __init__(self, bus: EventBus) -> None:
        self._bus = bus
        self.events: List[Event] = []

    def register_handler(self, type: Type[E], handler: EventHandler[E]) -> None:
        self._bus.register_handler(type, handler)

    def publish(self, event: E) -> None:
        self.events.append(event)
        self._bus.publish(event)

    def clear(self) -> None:
        self.events = []


class EventCounter(EventBus):
    def __init__(self, bus: EventBus) -> None:
        self._bus = bus
        self.counts: Dict[Type[Event], int] = {}

    def register_handler(self, type: Type[E], handler: EventHandler[E]) -> None:
        self._bus.register_handler(type, handler)

    def publish(self, event: E) -> None:
        count = self.counts.get(type(event))
        if count is None:
            self.counts[type(event)] = 1
        else:
            self.counts[type(event)] += 1
        self._bus.publish(event)

    def clear(self) -> None:
        self.counts = {}
