from abc import ABCMeta
from abc import abstractmethod
from typing import Type

from communication.messages import E
from communication.messages import EventHandler


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
