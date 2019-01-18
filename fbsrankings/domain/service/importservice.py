from fbsrankings.domain import SeasonFactory, TeamFactory, AffiliationFactory, GameFactory, SeasonRepository, TeamRepository, AffiliationRepository, GameRepository


class ImportService (object):
    def __init__(self, season_factory, team_factory, affiliation_factory, game_factory, season_repository, team_repository, affiliation_repository, game_repository):
        if not isinstance(season_factory, SeasonFactory):
            raise TypeError('season_factory must be of type SeasonFactory')
        self._season_factory = season_factory
        
        if not isinstance(team_factory, TeamFactory):
            raise TypeError('team_factory must be of type TeamFactory')
        self._team_factory = team_factory
        
        if not isinstance(affiliation_factory, AffiliationFactory):
            raise TypeError('affiliation_factory must be of type AffilaitionFactory')
        self._affiliation_factory = affiliation_factory
        
        if not isinstance(game_factory, GameFactory):
            raise TypeError('game_factory must be of type GameFactory')
        self._game_factory = game_factory
        
        if not isinstance(season_repository, SeasonRepository):
            raise TypeError('season_repository must be of type SeasonRepository')
        self._season_repository = season_repository
        
        if not isinstance(team_repository, TeamRepository):
            raise TypeError('team_repository must be of type TeamRepository')
        self._team_repository = team_repository
        
        if not isinstance(affiliation_repository, AffiliationRepository):
            raise TypeError('affiliation_repository must be of type AffiliationRepository')
        self._affiliation_repository = affiliation_repository
        
        if not isinstance(game_repository, GameRepository):
            raise TypeError('game_repository must be of type GameRepository')
        self._game_repository = game_repository
        
        self._seasons = {}
        self._teams = {}
        self._affiliations = {}
        self._games = {}
        
    @property
    def seasons(self):
        return self._seasons.values()
     
    @property
    def teams(self):
        return self._teams.values()
        
    @property
    def affiliations(self):
        return self._affiliations.values()
        
    @property
    def games(self):
        return self._games.values()
        
    def import_season(self, year):
        key = year
        
        season = self._seasons.get(key)
        if season is None:
            season = self._season_repository.find_by_year(year)
            if season is None:
                season = self._season_factory.register(year)
                self._season_repository.add(season)
            self._seasons[key] = season
            
        return season
        
    def import_team(self, name):
        key = name
        
        team = self._teams.get(key)
        if team is None:
            team = self._team_repository.find_by_name(name)
            if team is None:
                team = self._team_factory.register(name)
                self._team_repository.add(team)
            self._teams[key] = team
            
        return team
        
    def import_affiliation(self, season_ID, team_ID, subdivision):
        key = (season_ID, team_ID)
        
        affiliation = self._affiliations.get(key)
        if affiliation is None:
            affiliation = self._affiliation_repository.find_by_season_team(season_ID, team_ID)
            if affiliation is None:
                affiliation = self._affiliation_factory.register(season_ID, team_ID, subdivision)
                self._affiliation_repository.add(affiliation)
            self._affiliations[key] = affiliation
            
        return affiliation
        
    def import_game(self, season_ID, week, date_, season_section, home_team_ID, away_team_ID, notes):
        if home_team_ID < away_team_ID:
            key = (season_ID, season_section, week, home_team_ID, away_team_ID)
        else:
            key = (season_ID, season_section, week, away_team_ID, home_team_ID)
            
        game = self._games.get(key)
        if game is None:
            self._game_repository.find_by_season_teams(season_ID, season_section, week, home_team_ID, away_team_ID)
            if game is None:
                game = self._game_factory.schedule(season_ID, week, date_, season_section, home_team_ID, away_team_ID, notes)
                self._game_repository.add(game)
            self._games[key] = game
            
        return game
