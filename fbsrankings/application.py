import csv

from fbsrankings.domain.affiliation import Subdivision
from fbsrankings.domain.importservice import ImportService
from fbsrankings.infrastructure.sportsreference import SportsReference


class Application (object):
    def __init__(self, factory, repository):
        self._factory = factory
        self._repository = repository
        
        self._import_service = ImportService(self._factory, self._repository)
        self._sports_reference = SportsReference(self._import_service)
        
    def import_sports_reference_season(self, year, postseason_start_week, team_csv_filename, game_csv_filename):
        with open(team_csv_filename, 'r') as team_file:
            team_reader = csv.reader(team_file)
            self._sports_reference.import_teams_from_csv(year, team_reader)
            
        with open(game_csv_filename, 'r') as game_file:
            game_reader = csv.reader(game_file)
            self._sports_reference.import_games_from_csv(year, postseason_start_week, game_reader)

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
