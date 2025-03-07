from typing import Callable
from typing import Dict
from typing import Type

from communication.bus.domain.command import C
from communication.bus.domain.command import Command
from communication.bus.domain.command import CommandBus
from communication.bus.domain.command import CommandHandler
from communication.channel import Channel
from communication.channel import Payload
from serialization import Serializer


PayloadHandler = Callable[[Payload], None]


class CommandBridge(CommandBus):
    def __init__(
        self,
        channel: Channel,
        serializer: Serializer,
        topics: Dict[Type[Command], str],
    ) -> None:
        self._channel = channel
        self._serializer = serializer

        self._topics: Dict[Type[Command], str] = {}
        self._topics.update(topics)

        self._handlers: Dict[Type[Command], PayloadHandler] = {}

    def register_handler(self, type_: Type[C], handler: CommandHandler[C]) -> None:
        topic = self._topics.get(type_)
        if topic is None:
            raise ValueError(f"Unknown type: {type_}")

        def payload_handler(payload: Payload) -> None:
            command = self._serializer.deserialize(payload, type_)
            handler(command)

        existing = self._handlers.get(type_)
        if existing is not None:
            raise ValueError(f"A handler has already been registered for {type_}")
        self._handlers[type_] = payload_handler

        self._channel.subscribe(topic, payload_handler)

    def unregister_handler(self, type_: Type[C]) -> None:
        topic = self._topics.get(type_)
        if topic is None:
            raise ValueError(f"Unknown type: {type_}")

        payload_handler = self._handlers.pop(type_)
        if payload_handler is not None:
            self._channel.unsubscribe(topic, payload_handler)

    def send(self, command: C) -> None:
        type_ = type(command)
        topic = self._topics.get(type_)
        if topic is None:
            raise ValueError(f"Unknown type: {type_}")

        payload = self._serializer.serialize(command)
        self._channel.publish(topic, payload)
