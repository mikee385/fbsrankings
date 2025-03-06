from uuid import UUID

from dataclasses import dataclass

from communication.bus import Command


@dataclass(frozen=True)
class ImportSeasonByYearCommand(Command):
    id_: UUID
    year: int
