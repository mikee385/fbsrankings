from communication.channel.domain.channel import Channel
from communication.channel.domain.channel import Payload
from communication.channel.domain.channel import PayloadHandler


class MemoryChannel(Channel):
    def __init__(self) -> None:
        self._handlers: dict[str, list[PayloadHandler]] = {}

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
