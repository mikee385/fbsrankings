"""Error message classes for the fbsrankings package"""

from communication.messages import Event

from ..options import get_topic
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
    AffiliationDataValidationError: get_topic(AffiliationDataValidationError),
    FBSGameCountValidationError: get_topic(FBSGameCountValidationError),
    FCSGameCountValidationError: get_topic(FCSGameCountValidationError),
    GameDataValidationError: get_topic(GameDataValidationError),
    PostseasonGameCountValidationError: get_topic(PostseasonGameCountValidationError),
    SeasonDataValidationError: get_topic(SeasonDataValidationError),
    TeamDataValidationError: get_topic(TeamDataValidationError),
}
