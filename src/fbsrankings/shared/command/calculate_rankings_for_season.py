from typing import Union
from uuid import UUID

from dataclasses import dataclass

from fbsrankings.shared.messaging import Command


@dataclass(frozen=True)
class CalculateRankingsForSeasonCommand(Command):
    season_id_or_year: Union[UUID, int]
