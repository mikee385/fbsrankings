from fbsrankings.common import EventBus, EventCounter
from fbsrankings.domain import Subdivision, GameStatus, ImportService, ValidationService, RaiseBehavior, GameDataValidationError, FBSGameCountValidationError, FCSGameCountValidationError
from fbsrankings.infrastructure.sportsreference import Repository as SportsReference
from fbsrankings.infrastructure.memory import DataStore as MemoryDataStore
from fbsrankings.infrastructure.sqlite import DataStore as SqliteDataStore


class Application (object):
    def __init__(self, config):
        storage_type = config['settings']['storage_type']
        if storage_type == 'memory':
            self._data_store = MemoryDataStore()

        elif storage_type == 'sqlite':
            db_filename = config['settings']['sqlite_db_file']
            self._data_store = SqliteDataStore(db_filename)

        else:
            raise ValueError(f'Unknown storage type: {storage_type}')
                
        alternate_names = config.get('alternate_names')
        if alternate_names is None:
            alternate_names = {}
            
        self.seasons = []
        self._sports_reference = SportsReference(alternate_names)
        for season in config['seasons']:
            self.seasons.append(season['year'])
            self._sports_reference.add_source(
                season['year'],
                season['postseason_start_week'],
                season['source_type'],
                season['teams'],
                season['games']
            )
            
        self.validation_service = ValidationService(RaiseBehavior.ON_DEMAND)

        self.event_bus = EventCounter(EventBus())
        
    @property
    def errors(self):
        return self.validation_service.errors

    def import_season(self, year):
        self._sports_reference.load_from_source(year)
        
        with self._data_store.unit_of_work(self.event_bus) as unit_of_work:
            import_service = ImportService(unit_of_work.factory, unit_of_work.repository, self.validation_service)
            import_service.import_for_year(self._sports_reference, year)
        
            unit_of_work.commit()

    def calculate_rankings(self, year):
        pass
        
    def print_results(self):
        with self._data_store.queries() as repository:
            seasons = repository.season.all()
            print(f'Total Seasons: {len(seasons)}')
            for season in seasons:
                print()
                print(f'{season.year} Season:')
    
                affiliations = repository.affiliation.find_by_season(season)
                print(f'Total Teams: {len(affiliations)}')
                print(f'FBS Teams: {sum(x.subdivision == Subdivision.FBS for x in affiliations)}')
                print(f'FCS Teams: {sum(x.subdivision == Subdivision.FCS for x in affiliations)}')
    
                games = repository.game.find_by_season(season)
                print(f'Total Games: {len(games)}')
        
            canceled_games = [game for game in repository.game.all() if game.status == GameStatus.CANCELED]
            if canceled_games:
                print()
                print('Canceled Games:')
                for game in canceled_games:
                    print()
                    self._print_game_summary(repository, game)
        
            unknown_games = [game for game in repository.game.all() if game.status != GameStatus.COMPLETED and game.status != GameStatus.CANCELED]
            if unknown_games:
                print()
                print('Unknown Status:')
                for game in unknown_games:
                    print()
                    self._print_game_summary(repository, game)
        
    def print_errors(self):
        fbs_team_errors = []
        fcs_team_errors = []
        game_errors = []
        other_errors = []
        for error in self.errors:
            if isinstance(error, FBSGameCountValidationError):
                fbs_team_errors.append(error)
            elif isinstance(error, FCSGameCountValidationError):
                fcs_team_errors.append(error)
            elif isinstance(error, GameDataValidationError):
                game_errors.append(error)
            else:
                other_errors.append(error)

        with self._data_store.queries() as repository:
            if fbs_team_errors:
                print()
                print('FBS teams with too few games:')
                for error in fbs_team_errors:
                    season = repository.season.find_by_ID(error.season_ID)
                    team = repository.team.find_by_ID(error.team_ID)
                    print()
                    print(f'{season.year} {team.name}: {error.game_count}')
                
            if fcs_team_errors:
                print()
                print('FCS teams with too many games:')
                for error in fcs_team_errors:
                    season = repository.season.find_by_ID(error.season_ID)
                    team = repository.team.find_by_ID(error.team_ID)
                    print()
                    print(f'{season.year} {team.name}: {error.game_count}')
                
            if game_errors:
                print()
                print('Game Errors:')
                for error in game_errors:
                    game = repository.game.find_by_ID(error.game_ID)
                
                    print()
                    self._print_game_summary(repository, game)
                    print(f'For {error.attribute_name}, expected: {error.expected_value}, found: {error.attribute_value}')

        if other_errors:
            print()
            print('Other Errors:')
            for error in other_errors:
                print(error)
                
    def print_counts(self):
        print()
        print('Events:')
        if self.event_bus.counts:
            for event, count in self.event_bus.counts.items():
                print(f'{event.__name__}: {count}')
        else:
            print('None')
                
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
        
    def close(self):
        self.event_bus.clear()
        self._sports_reference.close()
        
    def __enter__(self):
        return self
        
    def __exit__(self, type, value, traceback):
        self.event_bus.clear()
        self._sports_reference.__exit__(type, value, traceback)
        return False
