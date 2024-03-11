"""Domain classes and methods for the fbsrankings package"""
from .model.affiliation import Affiliation
from .model.affiliation import AffiliationEventHandler
from .model.affiliation import AffiliationID
from .model.affiliation import AffiliationRepository
from .model.affiliation import Subdivision
from .model.game import Game
from .model.game import GameEventHandler
from .model.game import GameID
from .model.game import GameRepository
from .model.game import GameStatus
from .model.game import GameStatusError
from .model.ranking import GameRankingEventHandler
from .model.ranking import GameRankingRepository
from .model.ranking import GameRankingService
from .model.ranking import Ranking
from .model.ranking import RankingID
from .model.ranking import RankingValue
from .model.ranking import SeasonData
from .model.ranking import TeamRankingEventHandler
from .model.ranking import TeamRankingRepository
from .model.ranking import TeamRankingService
from .model.record import TeamRecord
from .model.record import TeamRecordEventHandler
from .model.record import TeamRecordID
from .model.record import TeamRecordRepository
from .model.record import TeamRecordValue
from .model.season import Season
from .model.season import SeasonEventHandler
from .model.season import SeasonID
from .model.season import SeasonRepository
from .model.season import SeasonSection
from .model.team import Team
from .model.team import TeamEventHandler
from .model.team import TeamID
from .model.team import TeamRepository
from .service.colley_matrix_ranking_service import ColleyMatrixRankingService
from .service.game_strength_ranking_service import GameStrengthRankingService
from .service.import_service import ImportService
from .service.record_service import TeamRecordService
from .service.simultaneous_wins_ranking_service import SimultaneousWinsRankingService
from .service.srs_ranking_service import SRSRankingService
from .service.strength_of_schedule_ranking_service import (
    StrengthOfScheduleRankingService,
)
from .service.validation_service import AffiliationDataValidationError
from .service.validation_service import FBSGameCountValidationError
from .service.validation_service import FCSGameCountValidationError
from .service.validation_service import GameDataValidationError
from .service.validation_service import MultipleValidationError
from .service.validation_service import RaiseBehavior
from .service.validation_service import SeasonDataValidationError
from .service.validation_service import TeamDataValidationError
from .service.validation_service import ValidationError
from .service.validation_service import ValidationService

__all__ = [
    "Affiliation",
    "AffiliationEventHandler",
    "AffiliationDataValidationError",
    "AffiliationID",
    "AffiliationRepository",
    "ColleyMatrixRankingService",
    "FBSGameCountValidationError",
    "FCSGameCountValidationError",
    "Game",
    "GameEventHandler",
    "GameDataValidationError",
    "GameID",
    "GameRankingEventHandler",
    "GameRankingRepository",
    "GameRankingService",
    "GameRepository",
    "GameStatus",
    "GameStatusError",
    "GameStrengthRankingService",
    "ImportService",
    "MultipleValidationError",
    "RaiseBehavior",
    "Ranking",
    "RankingID",
    "RankingValue",
    "Season",
    "SeasonData",
    "SeasonDataValidationError",
    "SeasonEventHandler",
    "SeasonID",
    "SeasonRepository",
    "SeasonSection",
    "SimultaneousWinsRankingService",
    "SRSRankingService",
    "StrengthOfScheduleRankingService",
    "Subdivision",
    "Team",
    "TeamDataValidationError",
    "TeamEventHandler",
    "TeamID",
    "TeamRankingEventHandler",
    "TeamRankingRepository",
    "TeamRankingService",
    "TeamRecord",
    "TeamRecordEventHandler",
    "TeamRecordID",
    "TeamRecordRepository",
    "TeamRecordValue",
    "TeamRepository",
    "TeamRecordService",
    "ValidationError",
    "ValidationService",
]
