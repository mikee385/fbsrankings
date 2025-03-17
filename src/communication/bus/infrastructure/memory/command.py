from typing import Any

from communication.bus.domain.command import CommandBus
from communication.messages import C
from communication.messages import Command
from communication.messages import CommandHandler


class MemoryCommandBus(CommandBus):
    def __init__(self) -> None:
        self._handlers: dict[type[Command], CommandHandler[Any]] = {}

    def register_handler(self, type_: type[C], handler: CommandHandler[C]) -> None:
        existing = self._handlers.get(type_)
        if existing is not None:
            raise ValueError(f"A handler has already been registered for {type_}")
        self._handlers[type_] = handler

    def unregister_handler(self, type_: type[C]) -> None:
        self._handlers.pop(type_)

    def send(self, command: C) -> None:
        handler = self._handlers.get(type(command))
        if handler is None:
            raise ValueError(f"No handler has been registered for {type(command)}")
        handler(command)
