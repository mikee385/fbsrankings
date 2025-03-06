from abc import ABCMeta
from abc import abstractmethod
from typing import Callable
from typing import Type
from typing import TypeVar
from uuid import UUID

from typing_extensions import Protocol


class Event(Protocol):
    event_id: UUID


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
