from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Tuple
from typing import Type
from typing import TypeVar

from fbsrankings.channel import EventChannel
from fbsrankings.channel import Payload
from fbsrankings.serialization.domain.serializer import Serializer
from fbsrankings.shared.error import Topics as ErrorTopics
from fbsrankings.shared.event import Topics as EventTopics
from fbsrankings.shared.messaging import Event
from fbsrankings.shared.messaging import EventBus


E = TypeVar("E", bound=Event, contravariant=True)


EventHandler = Callable[[E], None]


class PayloadHandler:
    def __init__(
        self,
        type_: Type[E],
        handler: EventHandler[E],
        serializer: Serializer,
    ) -> None:
        self._type = type_
        self._handler = handler
        self._serializer = serializer

    def __call__(self, payload: Payload) -> None:
        event = self._serializer.deserialize(payload, self._type)
        self._handler(event)


class SerializationEventBus(EventBus):
    def __init__(
        self,
        channel: EventChannel,
        serializer: Serializer,
    ) -> None:
        self._channel = channel
        self._serializer = serializer

        self._topics: Dict[Type[Event], str] = {}
        self._topics.update(EventTopics)
        self._topics.update(ErrorTopics)

        self._handlers: Dict[
            Tuple[Type[Event], EventHandler[Any]],
            List[PayloadHandler],
        ] = {}

    def register_handler(self, type_: Type[E], handler: EventHandler[E]) -> None:
        topic = self._topics.get(type_)
        if topic is None:
            raise ValueError(f"Unknown type: {type_}")

        key = (type_, handler)
        payload_handler = PayloadHandler(type_, handler, self._serializer)

        handlers = self._handlers.get(key)
        if handlers is not None:
            handlers.append(payload_handler)
        else:
            self._handlers[key] = [payload_handler]

        self._channel.subscribe(topic, payload_handler)

    def unregister_handler(self, type_: Type[E], handler: EventHandler[E]) -> None:
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
