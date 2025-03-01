from abc import ABCMeta
from abc import abstractmethod
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


class EventBus(metaclass=ABCMeta):
    @abstractmethod
    def register_handler(self, type_: Type[E], handler: EventHandler[E]) -> None:
        raise NotImplementedError

    @abstractmethod
    def unregister_handler(self, type_: Type[E], handler: EventHandler[E]) -> None:
        raise NotImplementedError

    @abstractmethod
    def publish(self, event: E) -> None:
        raise NotImplementedError


class MemoryEventBus(EventBus):
    def __init__(self) -> None:
        self._handlers: Dict[Type[Event], List[EventHandler[Any]]] = {}

    def register_handler(self, type_: Type[E], handler: EventHandler[E]) -> None:
        handlers = self._handlers.get(type_)
        if handlers is not None:
            handlers.append(handler)
        else:
            self._handlers[type_] = [handler]

    def unregister_handler(self, type_: Type[E], handler: EventHandler[E]) -> None:
        handlers = self._handlers.get(type_)
        if handlers is not None and handler in handlers:
            handlers.remove(handler)

    def publish(self, event: E) -> None:
        handlers = self._handlers.get(type(event))
        if handlers is not None:
            for handler in handlers:
                handler(event)
