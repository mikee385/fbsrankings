from uuid import UUID

from dataclasses import dataclass

from communication.bus import Command


@dataclass(frozen=True)
class ImportSeasonByYearCommand(Command):
    command_id: UUID
    year: int
