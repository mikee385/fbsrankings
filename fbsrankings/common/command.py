from typing import Dict, Type


class Command(object):
    pass


class CommandHandler(object):
    def handle(self, command: Command) -> None:
        raise NotImplementedError


class CommandBus(object):
    def __init__(self) -> None:
        self._handlers: Dict[Type[Command], CommandHandler] = {}

    def register_handler(self, type: type, handler: CommandHandler) -> None:
        existing = self._handlers.get(type)
        if existing is not None:
            raise ValueError(f"A handler has already been registered for {type}")
        else:
            self._handlers[type] = handler

    def unregister_handler(self, type: Type[Command], handler: CommandHandler) -> None:
        self._handlers.pop(type)

    def send(self, command: Command) -> None:
        handler = self._handlers.get(type(command))
        if handler is None:
            raise ValueError(f"No handler has been registered for {type(command)}")
        else:
            handler.handle(command)
