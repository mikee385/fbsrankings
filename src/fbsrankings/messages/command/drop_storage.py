from dataclasses import dataclass

from communication.messages import Command


@dataclass(frozen=True)
class DropStorageCommand(Command):
    command_id: str
