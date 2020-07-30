"""Domain classes and methods for the fbsrankings package"""
from .model.affiliation import Affiliation as Affiliation
from .model.affiliation import AffiliationID as AffiliationID
from .model.affiliation import AffiliationRepository as AffiliationRepository
from .model.affiliation import Subdivision as Subdivision
from .model.game import Game as Game
from .model.game import GameID as GameID
from .model.game import GameRepository as GameRepository
from .model.game import GameStatus as GameStatus
from .model.game import GameStatusError as GameStatusError
from .model.ranking import GameRankingRepository as GameRankingRepository
from .model.ranking import GameRankingService as GameRankingService
from .model.ranking import Ranking as Ranking
from .model.ranking import RankingID as RankingID
from .model.ranking import RankingValue as RankingValue
from .model.ranking import SeasonData as SeasonData
from .model.ranking import TeamRankingRepository as TeamRankingRepository
from .model.ranking import TeamRankingService as TeamRankingService
from .model.record import TeamRecord as TeamRecord
from .model.record import TeamRecordID as TeamRecordID
from .model.record import TeamRecordRepository as TeamRecordRepository
from .model.record import TeamRecordValue as TeamRecordValue
from .model.season import Season as Season
from .model.season import SeasonID as SeasonID
from .model.season import SeasonRepository as SeasonRepository
from .model.season import SeasonSection as SeasonSection
from .model.team import Team as Team
from .model.team import TeamID as TeamID
from .model.team import TeamRepository as TeamRepository
from .service.colley_matrix_ranking_service import (
    ColleyMatrixRankingService as ColleyMatrixRankingService,
)
from .service.game_strength_ranking_service import (
    GameStrengthRankingService as GameStrengthRankingService,
)
from .service.record_service import TeamRecordService as TeamRecordService
from .service.simultaneous_wins_ranking_service import (
    SimultaneousWinsRankingService as SimultaneousWinsRankingService,
)
from .service.srs_ranking_service import SRSRankingService as SRSRankingService
from .service.strength_of_schedule_ranking_service import (
    StrengthOfScheduleRankingService as StrengthOfScheduleRankingService,
)
from .service.validation_service import (
    AffiliationDataValidationError as AffiliationDataValidationError,
)
from .service.validation_service import (
    FBSGameCountValidationError as FBSGameCountValidationError,
)
from .service.validation_service import (
    FCSGameCountValidationError as FCSGameCountValidationError,
)
from .service.validation_service import (
    GameDataValidationError as GameDataValidationError,
)
from .service.validation_service import (
    MultipleValidationError as MultipleValidationError,
)
from .service.validation_service import RaiseBehavior as RaiseBehavior
from .service.validation_service import (
    SeasonDataValidationError as SeasonDataValidationError,
)
from .service.validation_service import (
    TeamDataValidationError as TeamDataValidationError,
)
from .service.validation_service import ValidationError as ValidationError
from .service.validation_service import ValidationService as ValidationService
