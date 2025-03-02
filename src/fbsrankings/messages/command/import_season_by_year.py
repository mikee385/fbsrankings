from dataclasses import dataclass

from communication.bus import Command


@dataclass(frozen=True)
class ImportSeasonByYearCommand(Command):
    year: int
