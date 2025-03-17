from typing import Any

from communication.bus.domain.event import EventBus
from communication.messages import E
from communication.messages import Event
from communication.messages import EventHandler


class MemoryEventBus(EventBus):
    def __init__(self) -> None:
        self._handlers: dict[type[Event], list[EventHandler[Any]]] = {}

    def register_handler(self, type_: type[E], handler: EventHandler[E]) -> None:
        handlers = self._handlers.get(type_)
        if handlers is not None:
            handlers.append(handler)
        else:
            self._handlers[type_] = [handler]

    def unregister_handler(self, type_: type[E], handler: EventHandler[E]) -> None:
        handlers = self._handlers.get(type_)
        if handlers is not None and handler in handlers:
            handlers.remove(handler)

    def publish(self, event: E) -> None:
        handlers = self._handlers.get(type(event))
        if handlers is not None:
            for handler in handlers:
                handler(event)
