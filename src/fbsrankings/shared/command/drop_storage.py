from dataclasses import dataclass

from fbsrankings.shared.messaging import Command


@dataclass(frozen=True)
class DropStorageCommand(Command):
    pass
