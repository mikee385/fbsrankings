from typing import Callable

from communication.bus import CommandBus
from communication.channel import Channel
from communication.channel import Payload
from communication.messages import C
from communication.messages import Command
from communication.messages import CommandHandler
from communication.messages import CommandTopicMapper
from serialization import Serializer


PayloadHandler = Callable[[Payload], None]


class CommandBridge(CommandBus):
    def __init__(
        self,
        channel: Channel,
        serializer: Serializer,
        topics: CommandTopicMapper,
    ) -> None:
        self._channel = channel
        self._serializer = serializer
        self._topics = topics

        self._handlers: dict[type[Command], PayloadHandler] = {}

    def _get_topic(self, type_: type[C]) -> str:
        topic = self._topics.get(type_)
        if topic is None:
            raise ValueError(f"Unknown type: {type_}")
        return topic

    def register_handler(self, type_: type[C], handler: CommandHandler[C]) -> None:
        topic = self._get_topic(type_)

        def payload_handler(payload: Payload) -> None:
            command = self._serializer.deserialize(payload, type_)
            handler(command)

        existing = self._handlers.get(type_)
        if existing is not None:
            raise ValueError(f"A handler has already been registered for {type_}")
        self._handlers[type_] = payload_handler

        self._channel.subscribe(topic, payload_handler)

    def unregister_handler(self, type_: type[C]) -> None:
        topic = self._get_topic(type_)

        payload_handler = self._handlers.pop(type_)
        if payload_handler is not None:
            self._channel.unsubscribe(topic, payload_handler)

    def send(self, command: C) -> None:
        type_ = type(command)
        topic = self._get_topic(type_)

        payload = self._serializer.serialize(command)
        self._channel.publish(topic, payload)
