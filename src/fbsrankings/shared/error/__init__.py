"""Shared error classes for the fbsrankings package"""

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
