"""Error message classes for the fbsrankings package"""

from communication.messages import Event

from .validation_pb2 import AffiliationDataValidationError
from .validation_pb2 import FBSGameCountValidationError
from .validation_pb2 import FCSGameCountValidationError
from .validation_pb2 import GameDataValidationError
from .validation_pb2 import PostseasonGameCountValidationError
from .validation_pb2 import SeasonDataValidationError
from .validation_pb2 import TeamDataValidationError


__all__ = [
    "AffiliationDataValidationError",
    "FBSGameCountValidationError",
    "FCSGameCountValidationError",
    "GameDataValidationError",
    "PostseasonGameCountValidationError",
    "SeasonDataValidationError",
    "TeamDataValidationError",
]

Topics: dict[type[Event], str] = {
    AffiliationDataValidationError: "fbsrankings/error/validation/affiliation_data",
    FBSGameCountValidationError: "fbsrankings/error/validation/fbs_game_count",
    FCSGameCountValidationError: "fbsrankings/error/validation/fcs_game_count",
    GameDataValidationError: "fbsrankings/error/validation/game_data",
    PostseasonGameCountValidationError: "fbsrankings/error/validation/postseason_game_count",
    SeasonDataValidationError: "fbsrankings/error/validation/season_data",
    TeamDataValidationError: "fbsrankings/error/validation/team_data",
}
