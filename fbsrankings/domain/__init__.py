"""Domain classes and methods for the fbsrankings package"""
from fbsrankings.domain.model.affiliation import Affiliation as Affiliation
from fbsrankings.domain.model.affiliation import AffiliationID as AffiliationID
from fbsrankings.domain.model.affiliation import (
    AffiliationRepository as AffiliationRepository,
)
from fbsrankings.domain.model.affiliation import Subdivision as Subdivision
from fbsrankings.domain.model.game import Game as Game
from fbsrankings.domain.model.game import GameID as GameID
from fbsrankings.domain.model.game import GameRepository as GameRepository
from fbsrankings.domain.model.game import GameStatus as GameStatus
from fbsrankings.domain.model.game import GameStatusError as GameStatusError
from fbsrankings.domain.model.ranking import (
    GameRankingRepository as GameRankingRepository,
)
from fbsrankings.domain.model.ranking import GameRankingService as GameRankingService
from fbsrankings.domain.model.ranking import Ranking as Ranking
from fbsrankings.domain.model.ranking import RankingID as RankingID
from fbsrankings.domain.model.ranking import RankingValue as RankingValue
from fbsrankings.domain.model.ranking import SeasonData as SeasonData
from fbsrankings.domain.model.ranking import (
    TeamRankingRepository as TeamRankingRepository,
)
from fbsrankings.domain.model.ranking import TeamRankingService as TeamRankingService
from fbsrankings.domain.model.season import Season as Season
from fbsrankings.domain.model.season import SeasonID as SeasonID
from fbsrankings.domain.model.season import SeasonRepository as SeasonRepository
from fbsrankings.domain.model.season import SeasonSection as SeasonSection
from fbsrankings.domain.model.team import Team as Team
from fbsrankings.domain.model.team import TeamID as TeamID
from fbsrankings.domain.model.team import TeamRepository as TeamRepository
from fbsrankings.domain.service.ranking.colley_matrix_ranking_service import (
    ColleyMatrixRankingService as ColleyMatrixRankingService,
)
from fbsrankings.domain.service.ranking.simultaneous_wins_ranking_service import (
    SimultaneousWinsRankingService as SimultaneousWinsRankingService,
)
from fbsrankings.domain.service.ranking.strength_of_schedule_ranking_service import (
    StrengthOfScheduleRankingService as StrengthOfScheduleRankingService,
)
from fbsrankings.domain.service.validation_service import (
    AffiliationDataValidationError as AffiliationDataValidationError,
)
from fbsrankings.domain.service.validation_service import (
    FBSGameCountValidationError as FBSGameCountValidationError,
)
from fbsrankings.domain.service.validation_service import (
    FCSGameCountValidationError as FCSGameCountValidationError,
)
from fbsrankings.domain.service.validation_service import (
    GameDataValidationError as GameDataValidationError,
)
from fbsrankings.domain.service.validation_service import (
    MultipleValidationError as MultipleValidationError,
)
from fbsrankings.domain.service.validation_service import RaiseBehavior as RaiseBehavior
from fbsrankings.domain.service.validation_service import (
    SeasonDataValidationError as SeasonDataValidationError,
)
from fbsrankings.domain.service.validation_service import (
    TeamDataValidationError as TeamDataValidationError,
)
from fbsrankings.domain.service.validation_service import (
    ValidationError as ValidationError,
)
from fbsrankings.domain.service.validation_service import (
    ValidationService as ValidationService,
)
