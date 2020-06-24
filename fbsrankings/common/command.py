from abc import ABCMeta
from typing import Any, Dict, Generic, Type, TypeVar

from typing_extensions import Protocol


class Command(metaclass=ABCMeta):
    pass


C = TypeVar("C", bound=Command, contravariant=True)


class CommandHandler(Generic[C], Protocol):
    def handle(self, command: C) -> None:
        raise NotImplementedError


class CommandBus(object):
    def __init__(self) -> None:
        self._handlers: Dict[Type[Command], CommandHandler[Any]] = {}

    def register_handler(self, type: Type[C], handler: CommandHandler[C]) -> None:
        existing = self._handlers.get(type)
        if existing is not None:
            raise ValueError(f"A handler has already been registered for {type}")
        else:
            self._handlers[type] = handler

    def unregister_handler(self, type: Type[C], handler: CommandHandler[C]) -> None:
        self._handlers.pop(type)

    def send(self, command: C) -> None:
        handler = self._handlers.get(type(command))
        if handler is None:
            raise ValueError(f"No handler has been registered for {type(command)}")
        else:
            handler.handle(command)
