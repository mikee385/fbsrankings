"""Error message classes for the fbsrankings package"""

from typing import Dict
from typing import Type

from communication.messages import Event

from .validation import AffiliationDataValidationError
from .validation import FBSGameCountValidationError
from .validation import FCSGameCountValidationError
from .validation import GameDataValidationError
from .validation import MultipleValidationError
from .validation import PostseasonGameCountValidationError
from .validation import SeasonDataValidationError
from .validation import TeamDataValidationError
from .validation import ValidationError


__all__ = [
    "AffiliationDataValidationError",
    "FBSGameCountValidationError",
    "FCSGameCountValidationError",
    "GameDataValidationError",
    "MultipleValidationError",
    "PostseasonGameCountValidationError",
    "SeasonDataValidationError",
    "TeamDataValidationError",
    "ValidationError",
]

Topics: Dict[Type[Event], str] = {
    AffiliationDataValidationError: "fbsrankings/error/validation/affiliation_data",
    FBSGameCountValidationError: "fbsrankings/error/validation/fbs_game_count",
    FCSGameCountValidationError: "fbsrankings/error/validation/fcs_game_count",
    GameDataValidationError: "fbsrankings/error/validation/game_data",
    MultipleValidationError: "fbsrankings/error/validation/multiple",
    PostseasonGameCountValidationError: "fbsrankings/error/validation/postseason_game_count",
    SeasonDataValidationError: "fbsrankings/error/validation/season_data",
    TeamDataValidationError: "fbsrankings/error/validation/team_data",
}
