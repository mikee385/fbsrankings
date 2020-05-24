from fbsrankings.domain import Repository
from fbsrankings.infrastructure.sportsreference import SeasonQueryHandler, TeamQueryHandler, AffiliationQueryHandler, GameQueryHandler


class QueryHandler (Repository):
    def __init__(self, data_source, repository):
        if not isinstance(repository, Repository):
            raise TypeError('repository must be of type Repository')
        
        super().__init__(
            SeasonQueryHandler(data_source, repository.season),
            TeamQueryHandler(data_source, repository.team),
            AffiliationQueryHandler(data_source, repository.affiliation),
            GameQueryHandler(data_source, repository.game)
        )
