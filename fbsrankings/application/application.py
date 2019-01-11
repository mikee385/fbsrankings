import os

from fbsrankings.domain import Subdivision, GameStatus, ImportService, ValidationService, CancelService
from fbsrankings.infrastructure import SportsReference

from fbsrankings.domain.service.validationservice import RaiseBehavior, DuplicateGameValidationError


class Application (object):
    def __init__(self, factory, repository, common_name_map):
        self._factory = factory
        self._repository = repository
        self._validation_service = ValidationService(RaiseBehavior.ON_DEMAND)
        self._import_service = ImportService(self._factory, self._repository)
        
        if common_name_map is not None:
            self._common_name_map = common_name_map
        else:
            self._common_name_map = {}
        
    def import_sports_reference_season(self, year, postseason_start_week, team_source, game_source):
        import_service = ImportService(self._factory, self._repository)
        validation_service = ValidationService()
        sports_reference = SportsReference(import_service, validation_service, self._common_name_map)
        
        if os.path.isfile(team_source) and os.path.isfile(game_source):
            sports_reference.import_season_csv_files(year, postseason_start_week, team_source, game_source)
        else:
            sports_reference.import_season_urls(year, postseason_start_week, team_source, game_source)
            
        cancel_service = CancelService(self._repository)
        cancel_service.cancel_past_games(year)

    def calculate_rankings(self, year):
        pass
        
    def display(self):
        seasons = self._repository.all_seasons()
        print(f'Total Seasons: {len(seasons)}')
        for season in seasons:
            print()
            print(f'{season.year} Season:')
    
            affiliations = self._repository.find_affiliations_by_season(season)
            print(f'Total Teams: {len(affiliations)}')
            print(f'FBS Teams: {sum(x.subdivision == Subdivision.FBS for x in affiliations)}')
            print(f'FCS Teams: {sum(x.subdivision == Subdivision.FCS for x in affiliations)}')
    
            games = self._repository.find_games_by_season(season)
            print(f'Total Games: {len(games)}')
        
        print()
        for game in self._repository.all_games():
            if game.status == GameStatus.CANCELED:
                print('Canceled Game:')
                self._print_game_summary(game)
            elif game.status != GameStatus.COMPLETED:
                print('Unknown Status')
                self._print_game_summary(game)
        
    def _print_game_summary(self, game):
        season = self._repository.find_season(game.season_ID)
        home_team = self._repository.find_team(game.home_team_ID)
        away_team = self._repository.find_team(game.away_team_ID)
        print(f'Year {season.year}, Week {game.week}')
        print(game.date)
        print(f'{home_team.name} vs. {away_team.name}')
        if game.home_team_score is not None and game.away_team_score is not None:
            print(f'{game.status}, {game.home_team_score} to {game.away_team_score}')
        else:
            print(game.status)
        print(game.notes)
        print()
