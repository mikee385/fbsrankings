from abc import ABCMeta
from abc import abstractmethod
from typing import Callable
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
