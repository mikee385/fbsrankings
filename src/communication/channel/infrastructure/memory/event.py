from typing import Dict
from typing import List

from communication.channel.domain.event import EventChannel
from communication.channel.domain.event import Payload
from communication.channel.domain.event import PayloadHandler


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
