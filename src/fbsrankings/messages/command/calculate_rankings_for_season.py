from typing import Union

from dataclasses import dataclass

from communication.messages import Command


@dataclass(frozen=True)
class CalculateRankingsForSeasonCommand(Command):
    command_id: str
    season_id_or_year: Union[str, int]
