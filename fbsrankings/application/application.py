from enum import Enum

from fbsrankings.domain import Subdivision, GameStatus, ImportService, ValidationService, CancelService
from fbsrankings.infrastructure import SportsReference

from fbsrankings.domain.service.validationservice import RaiseBehavior, DuplicateGameValidationError


class SourceType (Enum):
        CSV = 0
        URL = 1


class Application (object):
    def __init__(self, factory, repository, common_name_map):
        self._factory = factory
        self._repository = repository
        
        if common_name_map is not None:
            self._common_name_map = common_name_map
        else:
            self._common_name_map = {}
            
        self.errors = []
            
    def import_season_csv_files(self, year, postseason_start_week, team_csv_file, game_csv_file):
        self._import_season(SourceType.CSV, year, postseason_start_week, team_csv_file, game_csv_file)
        
    def import_season_urls(self, year, postseason_start_week, team_url, game_url):
        self._import_season(SourceType.URL, year, postseason_start_week, team_url, game_url)
        
    def _import_season(self, source_type, year, postseason_start_week, team_source, game_source):
        import_service = ImportService(self._factory, self._repository)
        validation_service = ValidationService(RaiseBehavior.ON_DEMAND)
        cancel_service = CancelService(self._repository)
        
        sports_reference = SportsReference(import_service, validation_service, self._common_name_map)
        
        if source_type == SourceType.CSV:
            sports_reference.import_season_csv_files(year, postseason_start_week, team_source, game_source)
        elif source_type == SourceType.URL:
            sports_reference.import_season_urls(year, postseason_start_week, team_source, game_source)
        else:
            raise ValueError(f'Unknown source type: {source_type}')
            
        self.errors.extend(validation_service.errors)
        cancel_service.cancel_past_games(year)

    def calculate_rankings(self, year):
        pass
        
    def print_results(self):
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
                print()
                print('Canceled Game:')
                self._print_game_summary(game)
            elif game.status != GameStatus.COMPLETED:
                
                print('Unknown Status')
                self._print_game_summary(game)
        
    def print_errors(self):
        duplicate_game_errors = []
        other_errors = []
        for error in self.errors:
            if isinstance(error, DuplicateGameValidationError):
                duplicate_game_errors.append(error)
            else:
                other_errors.append(error)

        if len(duplicate_game_errors) > 0:
            print()
            print('Duplicate Games:')
            for error in duplicate_game_errors:
                first_game = self._repository.find_game(error.first_game_ID)
                print()
                self._print_game_summary(first_game)
                second_game = self._repository.find_game(error.second_game_ID)
                print()
                self._print_game_summary(second_game)

        if len(other_errors) > 0:
            print()
            print('Other Errors:')
            for error in other_errors:
                print(error)

    def _print_game_summary(self, game):
        season = self._repository.find_season(game.season_ID)
        home_team = self._repository.find_team(game.home_team_ID)
        away_team = self._repository.find_team(game.away_team_ID)
        print(f'Year {season.year}, Week {game.week}')
        print(game.date)
        print(game.season_section)
        print(f'{home_team.name} vs. {away_team.name}')
        if game.home_team_score is not None and game.away_team_score is not None:
            print(f'{game.status}, {game.home_team_score} to {game.away_team_score}')
        else:
            print(game.status)
        print(game.notes)
