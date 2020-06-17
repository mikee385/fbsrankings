import json

from fbsrankings.application import Application
from fbsrankings.common import EventBus, EventCounter
from fbsrankings.domain import GameDataValidationError, FBSGameCountValidationError, FCSGameCountValidationError
from fbsrankings.query import AffiliationCountBySeasonQuery, CanceledGamesQuery, GameByIDQuery, GameCountBySeasonQuery, SeasonByIDQuery, SeasonsQuery, TeamByIDQuery, TeamCountBySeasonQuery


with open('config.json') as config_file:
    config = json.load(config_file)
    
event_bus = EventCounter(EventBus())

with Application(config, event_bus) as application:
    for year in application.seasons:
        break
        print(f'{year}: Importing Data')
        application.import_season(year)
        
        print(f'{year}: Calculating Rankings')
        application.calculate_rankings(year)

    print()
    
    seasons = application.query(SeasonsQuery()).seasons
    print(f'Total Seasons: {len(seasons)}')
    for season in seasons:
        print()
        print(f'{season.year} Season:')
    
        team_count = application.query(TeamCountBySeasonQuery(season.ID))
        print(f'Total Teams: {team_count.count}')
            
        affiliation_count = application.query(AffiliationCountBySeasonQuery(season.ID))
        print(f'FBS Teams: {affiliation_count.fbs_count}')
        print(f'FCS Teams: {affiliation_count.fcs_count}')
    
        game_count = application.query(GameCountBySeasonQuery(season.ID))
        print(f'Total Games: {game_count.count}')
        
    canceled_games = application.query(CanceledGamesQuery()).games
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

    fbs_team_errors = []
    fcs_team_errors = []
    game_errors = []
    other_errors = []
    for error in application.errors:
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
            season = application.query(SeasonByIDQuery(error.season_ID))
            team = application.query(TeamByIDQuery(error.team_ID))
            print(f'{season.year} {team.name}: {error.game_count}')
                
    if fcs_team_errors:
        print()
        print('FCS teams with too many games:')
        print()
        for error in fcs_team_errors:
            season = application.query(SeasonByIDQuery(error.season_ID))
            team = application.query(TeamByIDQuery(error.team_ID))
            print(f'{season.year} {team.name}: {error.game_count}')
                
    if game_errors:
        print()
        print('Game Errors:')
        for error in game_errors:
            game = application.query(GameByIDQuery(error.game_ID))
                
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

    print()
    print('Events:')
    print()
    if event_bus.counts:
        for event, count in event_bus.counts.items():
            print(f'{event.__name__}: {count}')
    else:
        print('None')
    
    print()
