from enum import Enum

from fbsrankings.domain import Subdivision, GameStatus, ImportService, ValidationService, CancelService, RaiseBehavior, GameDataValidationError, DuplicateGameValidationError, FBSGameCountValidationError, FCSGameCountValidationError
from fbsrankings.infrastructure import SportsReference
from fbsrankings.infrastructure.local import UnitOfWork


class SourceType (Enum):
        CSV = 0
        URL = 1


class Application (object):
    def __init__(self, unit_of_work, common_name_map):
        if not isinstance(unit_of_work, UnitOfWork):
            raise TypeError('unit_of_work must be of type UnitOfWork')
        self._unit_of_work = unit_of_work
        
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
        import_service = ImportService(self._unit_of_work.season_factory, self._unit_of_work.team_factory, self._unit_of_work.affiliation_factory, self._unit_of_work.game_factory, self._unit_of_work.season_repository, self._unit_of_work.team_repository, self._unit_of_work.affiliation_repository, self._unit_of_work.game_repository)
        validation_service = ValidationService(RaiseBehavior.ON_DEMAND)
        cancel_service = CancelService()
        
        sports_reference = SportsReference(import_service, validation_service, self._common_name_map)
        
        if source_type == SourceType.CSV:
            sports_reference.import_season_csv_files(year, postseason_start_week, team_source, game_source)
        elif source_type == SourceType.URL:
            sports_reference.import_season_urls(year, postseason_start_week, team_source, game_source)
        else:
            raise ValueError(f'Unknown source type: {source_type}')
            
        self.errors.extend(validation_service.errors)
        cancel_service.cancel_past_games(import_service.games)

    def calculate_rankings(self, year):
        pass
        
    def print_results(self):
        seasons = self._unit_of_work.season_repository.all()
        print(f'Total Seasons: {len(seasons)}')
        for season in seasons:
            print()
            print(f'{season.year} Season:')
    
            affiliations = self._unit_of_work.affiliation_repository.find_by_season(season)
            print(f'Total Teams: {len(affiliations)}')
            print(f'FBS Teams: {sum(x.subdivision == Subdivision.FBS for x in affiliations)}')
            print(f'FCS Teams: {sum(x.subdivision == Subdivision.FCS for x in affiliations)}')
    
            games = self._unit_of_work.game_repository.find_by_season(season)
            print(f'Total Games: {len(games)}')
        
        print()
        for game in self._unit_of_work.game_repository.all():
            if game.status == GameStatus.CANCELED:
                print()
                print('Canceled Game:')
                self._print_game_summary(game)
            elif game.status != GameStatus.COMPLETED:
                
                print('Unknown Status')
                self._print_game_summary(game)
        
    def print_errors(self):
        duplicate_game_errors = []
        fbs_team_errors = []
        fcs_team_errors = []
        game_errors = []
        other_errors = []
        for error in self.errors:
            if isinstance(error, DuplicateGameValidationError):
                duplicate_game_errors.append(error)
            elif isinstance(error, FBSGameCountValidationError):
                fbs_team_errors.append(error)
            elif isinstance(error, FCSGameCountValidationError):
                fcs_team_errors.append(error)
            elif isinstance(error, GameDataValidationError):
                game_errors.append(error)
            else:
                other_errors.append(error)

        if len(duplicate_game_errors) > 0:
            print()
            print('Duplicate Games:')
            for error in duplicate_game_errors:
                first_game = self._unit_of_work.game_repository.find_by_ID(error.first_game_ID)
                print()
                self._print_game_summary(first_game)
                second_game = self._unit_of_work.game_repository.find_by_ID(error.second_game_ID)
                print()
                self._print_game_summary(second_game)

        if len(fbs_team_errors) > 0:
            print()
            print('FBS teams with too few games:')
            for error in fbs_team_errors:
                season = self._unit_of_work.season_repository.find_by_ID(error.season_ID)
                team = self._unit_of_work.team_repository.find_by_ID(error.team_ID)
                print()
                print(f'{season.year} {team.name}: {error.game_count}')
                
        if len(fcs_team_errors) > 0:
            print()
            print('FCS teams with too many games:')
            for error in fcs_team_errors:
                season = self._unit_of_work.season_repository.find_by_ID(error.season_ID)
                team = self._unit_of_work.team_repository.find_by_ID(error.team_ID)
                print()
                print(f'{season.year} {team.name}: {error.game_count}')
                
        if len(game_errors) > 0:
            print()
            print('Game errors:')
            for error in game_errors:
                game = self._unit_of_work.game_repository.find_by_ID(error.game_ID)
                
                print()
                self._print_game_summary(game)
                print(f'For {error.attribute_name}, expected: {error.expected_value}, found: {error.attribute_value}')

        if len(other_errors) > 0:
            print()
            print('Other Errors:')
            for error in other_errors:
                print(error)

    def _print_game_summary(self, game):
        season = self._unit_of_work.season_repository.find_by_ID(game.season_ID)
        home_team = self._unit_of_work.team_repository.find_by_ID(game.home_team_ID)
        away_team = self._unit_of_work.team_repository.find_by_ID(game.away_team_ID)
        print(f'Year {season.year}, Week {game.week}')
        print(game.date)
        print(game.season_section)
        print(f'{home_team.name} vs. {away_team.name}')
        if game.home_team_score is not None and game.away_team_score is not None:
            print(f'{game.status}, {game.home_team_score} to {game.away_team_score}')
        else:
            print(game.status)
        print(game.notes)
