from fbsrankings.infrastructure.sportsreference import SeasonQueryHandler, TeamQueryHandler, AffiliationQueryHandler, GameQueryHandler


class QueryHandler (object):
    def __init__(self, data_source, repository):
        self.season = SeasonQueryHandler(data_source, repository.season)
        self.team = TeamQueryHandler(data_source, repository.team)
        self.affiliation = AffiliationQueryHandler(data_source, repository.affiliation)
        self.game = GameQueryHandler(data_source, repository.game)
