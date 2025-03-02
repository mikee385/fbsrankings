from typing import Union
from uuid import UUID

from dataclasses import dataclass

from communication.bus import Command


@dataclass(frozen=True)
class CalculateRankingsForSeasonCommand(Command):
    season_id_or_year: Union[UUID, int]
