from dataclasses import dataclass

from fbsrankings.shared.messaging import Command


@dataclass(frozen=True)
class ImportSeasonByYearCommand(Command):
    year: int
