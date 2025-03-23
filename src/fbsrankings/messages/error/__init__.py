"""Error message classes for the fbsrankings package"""

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
