from abc import ABCMeta
from abc import abstractmethod
from typing import Callable


Payload = bytes


PayloadHandler = Callable[[Payload], None]


class Channel(metaclass=ABCMeta):
    @abstractmethod
    def subscribe(self, topic: str, handler: PayloadHandler) -> None:
        raise NotImplementedError

    @abstractmethod
    def unsubscribe(self, topic: str, handler: PayloadHandler) -> None:
        raise NotImplementedError

    @abstractmethod
    def publish(self, topic: str, payload: Payload) -> None:
        raise NotImplementedError
