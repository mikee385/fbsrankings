"""Read-model for the in-memory repositories of the fbsrankings package"""

from fbsrankings.infrastructure.memory.read.affiliation_count_by_season import AffiliationCountBySeasonQueryHandler
from fbsrankings.infrastructure.memory.read.canceled_games import CanceledGamesQueryHandler
from fbsrankings.infrastructure.memory.read.game_by_id import GameByIDQueryHandler
from fbsrankings.infrastructure.memory.read.game_count_by_season import GameCountBySeasonQueryHandler
from fbsrankings.infrastructure.memory.read.season_by_id import SeasonByIDQueryHandler
from fbsrankings.infrastructure.memory.read.seasons import SeasonsQueryHandler
from fbsrankings.infrastructure.memory.read.team_by_id import TeamByIDQueryHandler
from fbsrankings.infrastructure.memory.read.team_count_by_season import TeamCountBySeasonQueryHandler
from fbsrankings.infrastructure.memory.read.query_manager import QueryManager
