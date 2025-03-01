from abc import ABCMeta
from abc import abstractmethod
from typing import Callable
from typing import Dict
from typing import List


Payload = bytes


PayloadHandler = Callable[[Payload], None]


class EventChannel(metaclass=ABCMeta):
    @abstractmethod
    def subscribe(self, topic: str, handler: PayloadHandler) -> None:
        raise NotImplementedError

    @abstractmethod
    def unsubscribe(self, topic: str, handler: PayloadHandler) -> None:
        raise NotImplementedError

    @abstractmethod
    def publish(self, topic: str, payload: Payload) -> None:
        raise NotImplementedError


class MemoryEventChannel(EventChannel):
    def __init__(self) -> None:
        self._handlers: Dict[str, List[PayloadHandler]] = {}

    def subscribe(self, topic: str, handler: PayloadHandler) -> None:
        handlers = self._handlers.get(topic)
        if handlers is not None:
            handlers.append(handler)
        else:
            self._handlers[topic] = [handler]

    def unsubscribe(self, topic: str, handler: PayloadHandler) -> None:
        handlers = self._handlers.get(topic)
        if handlers is not None and handler in handlers:
            handlers.remove(handler)

    def publish(self, topic: str, payload: Payload) -> None:
        handlers = self._handlers.get(topic)
        if handlers is not None:
            for handler in handlers:
                handler(payload)
