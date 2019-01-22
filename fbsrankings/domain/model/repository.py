from fbsrankings.domain import SeasonRepository, TeamRepository, AffiliationRepository, GameRepository


class Repository (object):
    def __init__(self, season_repository, team_repository, affiliation_repository, game_repository):
        if not isinstance(season_repository, SeasonRepository):
            raise TypeError('season_repository must be of type SeasonRepository')
        self.season = season_repository
        
        if not isinstance(team_repository, TeamRepository):
            raise TypeError('team_repository must be of type TeamRepository')
        self.team = team_repository
        
        if not isinstance(affiliation_repository, AffiliationRepository):
            raise TypeError('affiliation_repository must be of type AffiliationRepository')
        self.affiliation = affiliation_repository
        
        if not isinstance(game_repository, GameRepository):
            raise TypeError('game_repository must be of type GameRepository')
        self.game = game_repository
