from typing import Union
from uuid import UUID

from fbsrankings.common import Command


class CalculateRankingsForSeasonCommand(Command):
    def __init__(self, season_ID_or_year: Union[UUID, int]) -> None:
        self.season_ID_or_year = season_ID_or_year
