from typing import Any
from typing import Callable

from communication.bus import EventBus
from communication.channel import Channel
from communication.channel import Payload
from communication.messages import E
from communication.messages import Event
from communication.messages import EventHandler
from serialization import Serializer


PayloadHandler = Callable[[Payload], None]


class EventBridge(EventBus):
    def __init__(
        self,
        channel: Channel,
        serializer: Serializer,
        topics: dict[type[Event], str],
    ) -> None:
        self._channel = channel
        self._serializer = serializer

        self._topics: dict[type[Event], str] = {}
        self._topics.update(topics)

        self._handlers: dict[
            tuple[type[Event], EventHandler[Any]],
            list[PayloadHandler],
        ] = {}

    def register_handler(self, type_: type[E], handler: EventHandler[E]) -> None:
        topic = self._topics.get(type_)
        if topic is None:
            raise ValueError(f"Unknown type: {type_}")

        def payload_handler(payload: Payload) -> None:
            event = self._serializer.deserialize(payload, type_)
            handler(event)

        key = (type_, handler)
        handlers = self._handlers.get(key)
        if handlers is not None:
            handlers.append(payload_handler)
        else:
            self._handlers[key] = [payload_handler]

        self._channel.subscribe(topic, payload_handler)

    def unregister_handler(self, type_: type[E], handler: EventHandler[E]) -> None:
        topic = self._topics.get(type_)
        if topic is None:
            raise ValueError(f"Unknown type: {type_}")

        key = (type_, handler)
        handlers = self._handlers.get(key)
        if handlers is not None:
            payload_handler = handlers.pop()
            self._channel.unsubscribe(topic, payload_handler)

            if not handlers:
                del self._handlers[key]

    def publish(self, event: E) -> None:
        type_ = type(event)
        topic = self._topics.get(type_)
        if topic is None:
            raise ValueError(f"Unknown type: {type_}")

        payload = self._serializer.serialize(event)
        self._channel.publish(topic, payload)
