from abc import ABCMeta
from abc import abstractmethod

from communication.messages import C
from communication.messages import CommandHandler


class CommandBus(metaclass=ABCMeta):
    @abstractmethod
    def register_handler(self, type_: type[C], handler: CommandHandler[C]) -> None:
        raise NotImplementedError

    @abstractmethod
    def unregister_handler(self, type_: type[C]) -> None:
        raise NotImplementedError

    @abstractmethod
    def send(self, command: C) -> None:
        raise NotImplementedError
