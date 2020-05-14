from fbsrankings.domain import GameStatus, Factory, Repository
from fbsrankings.domain.service.validationservice import ValidationService


class ImportService (object):
    def __init__(self, factory, repository, validation_service):
        if not isinstance(factory, Factory):
            raise TypeError('factory must be of type Factory')
        self._factory = factory
        
        if not isinstance(repository, Repository):
            raise TypeError('repository must be of typeRepository')
        self._repository = repository
        
        if validation_service is not None and not isinstance(validation_service, ValidationService):
            raise TypeError('validation_service must be of type ValidationService')
        self._validation_service = validation_service
        
        self._seasons = {}
        self._teams = {}
        self._affiliations = {}
        self._games = {}
        
    def import_for_year(self, source, year):
        source_season = source.season.find_by_year(year)
        self.import_season(year)
    
        affiliations = []
        source_affiliations = source.affiliation.find_by_season(source_season)
        for source_affiliation in source_affiliations:
            source_team = source.team.find_by_ID(source_affiliation.team_ID)
            self.import_team(source_team.name)
            
            affiliation = self.import_affiliation(year, source_team.name, source_affiliation.subdivision)
            affiliations.append(affiliation)
            
        games = []
        source_games = source.game.find_by_season(source_season)
        for source_game in source_games:
            source_home_team = source.team.find_by_ID(source_game.home_team_ID)
            source_away_team = source.team.find_by_ID(source_game.away_team_ID)
            
            game = self.import_game(year, source_game.week, source_game.date, source_game.season_section, source_home_team.name, source_away_team.name, source_game.home_team_score, source_game.away_team_score, source_game.status, source_game.notes)
            games.append(game)
            
        if self._validation_service is not None:
            self._validation_service.validate_games(affiliations, games)
            
    def import_season(self, year):
        key = year
        
        season = self._seasons.get(key)
        if season is None:
            season = self._repository.season.find_by_year(year)
            if season is None:
                season = self._factory.season.register(year)
            self._seasons[key] = season
            
        if self._validation_service is not None:
            self._validation_service.validate_season_data(season, year)
            
        return season
        
    def import_team(self, name):
        key = name
        
        team = self._teams.get(key)
        if team is None:
            team = self._repository.team.find_by_name(name)
            if team is None:
                team = self._factory.team.register(name)
            self._teams[key] = team
            
        if self._validation_service is not None:
            self._validation_service.validate_team_data(team, name)
            
        return team
        
    def import_affiliation(self, year, team_name, subdivision):
        season = self.import_season(year)
        team = self.import_team(team_name)
        
        key = (season.ID, team.ID)
        
        affiliation = self._affiliations.get(key)
        if affiliation is None:
            affiliation = self._repository.affiliation.find_by_season_team(season.ID, team.ID)
            if affiliation is None:
                affiliation = self._factory.affiliation.register(season.ID, team.ID, subdivision)
            self._affiliations[key] = affiliation
            
        if self._validation_service is not None:
            self._validation_service.validate_affiliation_data(affiliation, season.ID, team.ID, affiliation.subdivision)
            
        return affiliation
        
    def import_game(self, year, week, date_, season_section, home_team_name, away_team_name, home_team_score, away_team_score, status, notes):
        season = self.import_season(year)
        home_team = self.import_team(home_team_name)
        away_team = self.import_team(away_team_name)
        
        if home_team.ID < away_team.ID:
            key = (season.ID, week, home_team.ID, away_team.ID)
        else:
            key = (season.ID, week, away_team.ID, home_team.ID)
            
        game = self._games.get(key)
        if game is None:
            game = self._repository.game.find_by_season_teams(season.ID, week, home_team.ID, away_team.ID)
            if game is None:
                game = self._factory.game.schedule(season.ID, week, date_, season_section, home_team.ID, away_team.ID, notes)
            self._games[key] = game
            
        if date_ != game.date:
            game.reschedule(week, date_)
            
        if status == GameStatus.CANCELED and game.status != GameStatus.CANCELED:
            game.cancel()
        
        if status == GameStatus.COMPLETED and game.status != GameStatus.COMPLETED:
            game.complete(home_team_score, away_team_score)
                
        if notes != game.notes:
            game.update_notes(notes)
            
        if self._validation_service is not None:
            self._validation_service.validate_game_data(game, season.ID, week, date_, season_section, home_team.ID, away_team.ID, home_team_score, away_team_score, game.status, notes)
            
        return game
