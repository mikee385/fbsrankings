from uuid import UUID

from dataclasses import dataclass

from communication.messages import Command


@dataclass(frozen=True)
class ImportSeasonByYearCommand(Command):
    command_id: UUID
    year: int
