"""Command message classes for the fbsrankings package"""

from typing import Dict
from typing import Type

from communication.messages import Command

from .calculate_rankings_for_season import CalculateRankingsForSeasonCommand
from .drop_storage import DropStorageCommand
from .import_season_by_year import ImportSeasonByYearCommand


__all__ = [
    "CalculateRankingsForSeasonCommand",
    "DropStorageCommand",
    "ImportSeasonByYearCommand",
]

Topics: Dict[Type[Command], str] = {
    CalculateRankingsForSeasonCommand: "fbsrankings/command/calculate_rankings_for_season",
    DropStorageCommand: "fbsrankings/command/drop_storage",
    ImportSeasonByYearCommand: "fbsrankings/command/import_season_by_year",
}
