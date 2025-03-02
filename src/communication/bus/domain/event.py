from abc import ABCMeta
from abc import abstractmethod
from typing import Callable
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
