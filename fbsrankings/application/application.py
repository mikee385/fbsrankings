from enum import Enum

from fbsrankings.common import EventBus, EventRecorder
from fbsrankings.domain import Subdivision, GameStatus, ImportService, ValidationService, CancelService, RaiseBehavior, GameDataValidationError, DuplicateGameValidationError, FBSGameCountValidationError, FCSGameCountValidationError
from fbsrankings.infrastructure import SportsReference
from fbsrankings.infrastructure import UnitOfWorkFactory


class SourceType (Enum):
        CSV = 0
        URL = 1


class Application (object):
    def __init__(self, unit_of_work_factory, common_name_map):
        if not isinstance(unit_of_work_factory, UnitOfWorkFactory):
            raise TypeError('unit_of_work_factory must be of type UnitOfWorkFactory')
        self._unit_of_work_factory = unit_of_work_factory
        
        if common_name_map is not None:
            self._common_name_map = common_name_map
        else:
            self._common_name_map = {}
        
        self.event_bus = EventBus()
        self.errors = []
            
    def import_season_csv_files(self, year, postseason_start_week, team_csv_file, game_csv_file):
        self._import_season(SourceType.CSV, year, postseason_start_week, team_csv_file, game_csv_file)
        
    def import_season_urls(self, year, postseason_start_week, team_url, game_url):
        self._import_season(SourceType.URL, year, postseason_start_week, team_url, game_url)
        
    def _import_season(self, source_type, year, postseason_start_week, team_source, game_source):
        event_bus = EventRecorder(EventBus())
        unit_of_work = self._unit_of_work_factory.create(event_bus)
        
        import_service = ImportService(unit_of_work.factory, unit_of_work.repository)
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
        
        unit_of_work.commit()
        
        for event_type in event_bus.types:
            self.event_bus.register_type(event_type)
        
        for event in event_bus.events:
            self.event_bus.raise_event(event)

    def calculate_rankings(self, year):
        pass
        
    def print_results(self):
        event_bus = EventRecorder(EventBus())
        unit_of_work = self._unit_of_work_factory.create(event_bus)
        
        seasons = unit_of_work.repository.season.all()
        print(f'Total Seasons: {len(seasons)}')
        for season in seasons:
            print()
            print(f'{season.year} Season:')
    
            affiliations = unit_of_work.repository.affiliation.find_by_season(season)
            print(f'Total Teams: {len(affiliations)}')
            print(f'FBS Teams: {sum(x.subdivision == Subdivision.FBS for x in affiliations)}')
            print(f'FCS Teams: {sum(x.subdivision == Subdivision.FCS for x in affiliations)}')
    
            games = unit_of_work.repository.game.find_by_season(season)
            print(f'Total Games: {len(games)}')
        
        canceled_games = [game for game in unit_of_work.repository.game.all() if game.status == GameStatus.CANCELED]
        if canceled_games:
            print()
            print('Canceled Game:')
            for game in canceled_games:
                print()
                self._print_game_summary(unit_of_work.repository, game)
        
        unknown_games = [game for game in unit_of_work.repository.game.all() if game.status != GameStatus.COMPLETED and game.status != GameStatus.CANCELED]
        if unknown_games:
            print()
            print('Unknown Status:')
            for game in unknown_games:
                print()
                self._print_game_summary(unit_of_work.repository, game)
                
        if event_bus.events:
            raise ValueError('Domain should not have been modified during print_results')
        
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

        event_bus = EventRecorder(EventBus())
        unit_of_work = self._unit_of_work_factory.create(event_bus)
        
        if duplicate_game_errors:
            print()
            print('Duplicate Games:')
            for error in duplicate_game_errors:
                first_game = unit_of_work.repository.game.find_by_ID(error.first_game_ID)
                print()
                self._print_game_summary(unit_of_work.repository, first_game)
                second_game = unit_of_work.repository.game.find_by_ID(error.second_game_ID)
                print()
                self._print_game_summary(unit_of_work.repository, second_game)

        if fbs_team_errors:
            print()
            print('FBS teams with too few games:')
            for error in fbs_team_errors:
                season = unit_of_work.repository.season.find_by_ID(error.season_ID)
                team = unit_of_work.repository.team.find_by_ID(error.team_ID)
                print()
                print(f'{season.year} {team.name}: {error.game_count}')
                
        if fcs_team_errors:
            print()
            print('FCS teams with too many games:')
            for error in fcs_team_errors:
                season = unit_of_work.repository.season.find_by_ID(error.season_ID)
                team = unit_of_work.repository.team.find_by_ID(error.team_ID)
                print()
                print(f'{season.year} {team.name}: {error.game_count}')
                
        if game_errors:
            print()
            print('Game errors:')
            for error in game_errors:
                game = unit_of_work.repository.game.find_by_ID(error.game_ID)
                
                print()
                self._print_game_summary(unit_of_work.repository, game)
                print(f'For {error.attribute_name}, expected: {error.expected_value}, found: {error.attribute_value}')

        if other_errors:
            print()
            print('Other Errors:')
            for error in other_errors:
                print(error)
                
        if event_bus.events:
            raise ValueError('Domain should not have been modified during print_errors')

    def _print_game_summary(self, repository, game):
        season = repository.season.find_by_ID(game.season_ID)
        home_team = repository.team.find_by_ID(game.home_team_ID)
        away_team = repository.team.find_by_ID(game.away_team_ID)
        print(f'Year {season.year}, Week {game.week}')
        print(game.date)
        print(game.season_section)
        print(f'{home_team.name} vs. {away_team.name}')
        if game.home_team_score is not None and game.away_team_score is not None:
            print(f'{game.status}, {game.home_team_score} to {game.away_team_score}')
        else:
            print(game.status)
        print(game.notes)
