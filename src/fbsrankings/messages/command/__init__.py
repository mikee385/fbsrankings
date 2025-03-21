"""Command message classes for the fbsrankings package"""

from communication.messages import Command

from ..options import get_topic
from .calculate_rankings_for_season_pb2 import CalculateRankingsForSeasonCommand
from .drop_storage_pb2 import DropStorageCommand
from .import_season_by_year_pb2 import ImportSeasonByYearCommand


__all__ = [
    "CalculateRankingsForSeasonCommand",
    "DropStorageCommand",
    "ImportSeasonByYearCommand",
]

Topics: dict[type[Command], str] = {
    CalculateRankingsForSeasonCommand: get_topic(CalculateRankingsForSeasonCommand),
    DropStorageCommand: get_topic(DropStorageCommand),
    ImportSeasonByYearCommand: get_topic(ImportSeasonByYearCommand),
}
