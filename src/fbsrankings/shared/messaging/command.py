from abc import ABCMeta
from abc import abstractmethod
from typing import Any
from typing import Callable
from typing import Dict
from typing import Type
from typing import TypeVar


class Command(metaclass=ABCMeta):  # noqa: B024
    pass


C = TypeVar("C", bound=Command, contravariant=True)


CommandHandler = Callable[[C], None]


class CommandBus(metaclass=ABCMeta):
    @abstractmethod
    def register_handler(self, type_: Type[C], handler: CommandHandler[C]) -> None:
        raise NotImplementedError

    @abstractmethod
    def unregister_handler(self, type_: Type[C]) -> None:
        raise NotImplementedError

    @abstractmethod
    def send(self, command: C) -> None:
        raise NotImplementedError


class MemoryCommandBus(CommandBus):
    def __init__(self) -> None:
        self._handlers: Dict[Type[Command], CommandHandler[Any]] = {}

    def register_handler(self, type_: Type[C], handler: CommandHandler[C]) -> None:
        existing = self._handlers.get(type_)
        if existing is not None:
            raise ValueError(f"A handler has already been registered for {type_}")
        self._handlers[type_] = handler

    def unregister_handler(self, type_: Type[C]) -> None:
        self._handlers.pop(type_)

    def send(self, command: C) -> None:
        handler = self._handlers.get(type(command))
        if handler is None:
            raise ValueError(f"No handler has been registered for {type(command)}")
        handler(command)
