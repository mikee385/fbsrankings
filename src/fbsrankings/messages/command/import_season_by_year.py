from dataclasses import dataclass

from communication.messages import Command


@dataclass(frozen=True)
class ImportSeasonByYearCommand(Command):
    command_id: str
    year: int
