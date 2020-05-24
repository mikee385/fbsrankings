"""Repositories for querying sportsreference.com for the domain classes of the fbsrankings package"""

from fbsrankings.infrastructure.sportsreference.season import SeasonQueryHandler
from fbsrankings.infrastructure.sportsreference.team import TeamQueryHandler
from fbsrankings.infrastructure.sportsreference.affiliation import AffiliationQueryHandler
from fbsrankings.infrastructure.sportsreference.game import GameQueryHandler
from fbsrankings.infrastructure.sportsreference.handler import QueryHandler
from fbsrankings.infrastructure.sportsreference.datasource import DataSource, QueryProvider
