from fbsrankings.common import QueryBus, EventBus, EventCounter
from fbsrankings.domain import ValidationService, RaiseBehavior, GameDataValidationError, FBSGameCountValidationError, FCSGameCountValidationError
from fbsrankings.infrastructure import UnitOfWork
from fbsrankings.infrastructure.sportsreference import SportsReference
from fbsrankings.infrastructure.memory import DataSource as MemoryDataSource
from fbsrankings.infrastructure.sqlite import DataSource as SqliteDataSource
from fbsrankings.query import AffiliationCountBySeasonQuery, CanceledGamesQuery, GameByIDQuery, GameCountBySeasonQuery, SeasonByIDQuery, SeasonsQuery, TeamByIDQuery, TeamCountBySeasonQuery


class Application (object):
    def __init__(self, config):
        storage_type = config['settings']['storage_type']
        if storage_type == 'memory':
            self._data_source = MemoryDataSource()

        elif storage_type == 'sqlite':
            db_filename = config['settings']['sqlite_db_file']
            self._data_source = SqliteDataSource(db_filename)

        else:
            raise ValueError(f'Unknown storage type: {storage_type}')
                
        alternate_names = config.get('alternate_names')
        if alternate_names is None:
            alternate_names = {}
            
        self.validation_service = ValidationService(RaiseBehavior.ON_DEMAND)
            
        self.seasons = []
        self._sports_reference = SportsReference(alternate_names, self.validation_service)
        for season in config['seasons']:
            self.seasons.append(season['year'])
            self._sports_reference.add_source(
                season['year'],
                season['postseason_start_week'],
                season['source_type'],
                season['teams'],
                season['games']
            )

        self._query_bus = QueryBus()
        self._query_handler = self._data_source.query_handler(self._query_bus)
        
        self._event_bus = EventCounter(EventBus())
        
    @property
    def errors(self):
        return self.validation_service.errors

    def import_season(self, year):
        with UnitOfWork(self._data_source, self._event_bus) as unit_of_work:
            self._sports_reference.import_season(year, unit_of_work)
        
            unit_of_work.commit()

    def calculate_rankings(self, year):
        pass
        
    def print_results(self):
        seasons = self._query_bus.query(SeasonsQuery()).seasons
        print(f'Total Seasons: {len(seasons)}')
        for season in seasons:
            print()
            print(f'{season.year} Season:')
    
            team_count = self._query_bus.query(TeamCountBySeasonQuery(season.ID))
            print(f'Total Teams: {team_count.count}')
            
            affiliation_count = self._query_bus.query(AffiliationCountBySeasonQuery(season.ID))
            print(f'FBS Teams: {affiliation_count.fbs_count}')
            print(f'FCS Teams: {affiliation_count.fcs_count}')
    
            game_count = self._query_bus.query(GameCountBySeasonQuery(season.ID))
            print(f'Total Games: {game_count.count}')
        
        canceled_games = self._query_bus.query(CanceledGamesQuery()).games
        if canceled_games:
            print()
            print('Canceled Games:')
            for game in canceled_games:
                print()
                print(f'Year {game.year}, Week {game.week}')
                print(game.date)
                print(game.season_section)
                print(f'{game.home_team_name} vs. {game.away_team_name}')
                print(game.notes)
        
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

        if fbs_team_errors:
            print()
            print('FBS teams with too few games:')
            print()
            for error in fbs_team_errors:
                season = self._query_bus.query(SeasonByIDQuery(error.season_ID))
                team = self._query_bus.query(TeamByIDQuery(error.team_ID))
                print(f'{season.year} {team.name}: {error.game_count}')
                
        if fcs_team_errors:
            print()
            print('FCS teams with too many games:')
            print()
            for error in fcs_team_errors:
                season = self._query_bus.query(SeasonByIDQuery(error.season_ID))
                team = self._query_bus.query(TeamByIDQuery(error.team_ID))
                print(f'{season.year} {team.name}: {error.game_count}')
                
        if game_errors:
            print()
            print('Game Errors:')
            for error in game_errors:
                game = self._query_bus.query(GameByIDQuery(error.game_ID))
                
                print()
                print(f'Year {game.year}, Week {game.week}')
                print(game.date)
                print(game.season_section)
                print(f'{game.home_team_name} vs. {game.away_team_name}')
                if game.home_team_score is not None and game.away_team_score is not None:
                    print(f'{game.status}, {game.home_team_score} to {game.away_team_score}')
                else:
                    print(game.status)
                print(game.notes)
                print(f'For {error.attribute_name}, expected: {error.expected_value}, found: {error.attribute_value}')

        if other_errors:
            print()
            print('Other Errors:')
            print()
            for error in other_errors:
                print(error)
                
    def print_counts(self):
        print()
        print('Events:')
        print()
        if self._event_bus.counts:
            for event, count in self._event_bus.counts.items():
                print(f'{event.__name__}: {count}')
        else:
            print('None')
        
    def close(self):
        self._query_handler.close()
        self._event_bus.clear()
        
    def __enter__(self):
        return self
        
    def __exit__(self, type, value, traceback):
        self.close()
        return False
