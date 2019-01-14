from fbsrankings.domain import SeasonFactory, SeasonRepository, TeamFactory, TeamRepository, AffiliationFactory, AffiliationRepository, GameFactory, GameRepository


class ImportService (object):
    def __init__(self, factory, repository):
        if not isinstance(factory, SeasonFactory):
            raise TypeError('factory must be of type SeasonFactory')
        if not isinstance(factory, TeamFactory):
            raise TypeError('factory must be of type TeamFactory')
        if not isinstance(factory, AffiliationFactory):
            raise TypeError('factory must be of type AffiliationFactory')
        if not isinstance(factory, GameFactory):
            raise TypeError('factory must be of type GameFactory')
        self._factory = factory
        
        if not isinstance(repository, SeasonRepository):
            raise TypeError('repository must be of type SeasonRepository')
        if not isinstance(repository, TeamRepository):
            raise TypeError('repository must be of type TeamRepository')
        if not isinstance(repository, AffiliationRepository):
            raise TypeError('repository must be of type AffiliationRepository')
        if not isinstance(repository, GameRepository):
            raise TypeError('repository must be of type GameRepository')
        self._repository = repository
        
        self._seasons = {}
        self._teams = {}
        self._affiliations = {}
        self._games = {}
        
    def seasons(self):
        return self._seasons.values()
        
    def teams(self):
        return self._teams.values()
        
    def affiliations(self):
        return self._affiliations.values()
        
    def games(self):
        return self._games.values()
        
    def import_season(self, year):
        key = year
        
        season = self._seasons.get(key)
        if season is None:
            season = self._repository.find_season_by_year(year)
            if season is None:
                season = self._factory.new_season(year)
                self._repository.add_season(season)
            self._seasons[key] = season
            
        return season
        
    def import_team(self, name):
        key = name
        
        team = self._teams.get(key)
        if team is None:
            team = self._repository.find_team_by_name(name)
            if team is None:
                team = self._factory.new_team(name)
                self._repository.add_team(team)
            self._teams[key] = team
            
        return team
        
    def import_affiliation(self, season_ID, team_ID, subdivision):
        key = (season_ID, team_ID)
        
        affiliation = self._affiliations.get(key)
        if affiliation is None:
            affiliation = self._repository.find_affiliation_by_season_team(season_ID, team_ID)
            if affiliation is None:
                affiliation = self._factory.new_affiliation(season_ID, team_ID, subdivision)
                self._repository.add_affiliation(affiliation)
            self._affiliations[key] = affiliation
            
        return affiliation
        
    def import_game(self, season_ID, week, date_, season_section, home_team_ID, away_team_ID, notes):
        if home_team_ID < away_team_ID:
            key = (season_ID, season_section, week, home_team_ID, away_team_ID)
        else:
            key = (season_ID, season_section, week, away_team_ID, home_team_ID)
            
        game = self._games.get(key)
        if game is None:
            self._repository.find_game_by_season_teams(season_ID, season_section, week, home_team_ID, away_team_ID)
            if game is None:
                game = self._factory.new_game(season_ID, week, date_, season_section, home_team_ID, away_team_ID, notes)
                self._repository.add_game(game)
            self._games[key] = game
            
        return game
