import csv

from fbsrankings.domain import Subdivision,  GameStatus, ImportService, CancelService
from fbsrankings.infrastructure import SportsReference


class Application (object):
    def __init__(self, factory, repository):
        self._factory = factory
        self._repository = repository
        
    def import_sports_reference_season(self, year, postseason_start_week, team_csv_filename, game_csv_filename):
        import_service = ImportService(self._factory, self._repository)
        sports_reference = SportsReference(import_service)
        sports_reference.import_season_csv_files(year, postseason_start_week, team_csv_filename, game_csv_filename)
            
        cancel_service = CancelService(self._repository)
        cancel_service.cancel_past_games(year)

    def calculate_rankings(self, year):
        pass
        
    def display(self):
        seasons = self._repository.all_seasons()
        print('Total Seasons: ' + str(len(seasons)))
        for season in seasons:
            print()
            print(str(season.year) + ' Season:')
    
            affiliations = self._repository.find_affiliations_by_season(season)
            print('Total Teams: ' + str(len(affiliations)))
            print('FBS Teams: ' + str(sum(x.subdivision == Subdivision.FBS for x in affiliations)))
            print('FCS Teams: ' + str(sum(x.subdivision == Subdivision.FCS for x in affiliations)))
    
            games = self._repository.find_games_by_season(season)
            print('Total Games: ' + str(len(games)))
        
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
        print('Year ' + str(season.year) + ', Week ' + str(game.week))
        print(game.date)
        print(home_team.name + ' vs. ' + away_team.name)
        if game.home_team_score is not None and game.away_team_score is not None:
            print(str(game.status) + ', ' + str(game.home_team_score) + ' to ' + str(game.away_team_score))
        else:
            print(game.status)
        print()
