from dataclasses import dataclass

from communication.bus import Command


@dataclass(frozen=True)
class DropStorageCommand(Command):
    pass
