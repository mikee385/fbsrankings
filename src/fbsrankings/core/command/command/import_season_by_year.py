from dataclasses import dataclass

from fbsrankings.common import Command


@dataclass(frozen=True)
class ImportSeasonByYearCommand(Command):
    year: int
