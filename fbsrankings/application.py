import csv

from fbsrankings.domain.affiliation import Subdivision
from fbsrankings.infrastructure.sportsreference import SportsReference


class Application (object):
    def __init__(self, repository):
        self._repository = repository
        self._sportsreference = SportsReference(repository)
        
    def ImportSportsReferenceSeason(self, year, postseason_start_week, team_csv_filename, game_csv_filename):
        with open(team_csv_filename, 'r') as team_file:
            team_reader = csv.reader(team_file)
            self._sportsreference.ImportTeamsFromCsv(year, team_reader)
            
        with open(game_csv_filename, 'r') as game_file:
            game_reader = csv.reader(game_file)
            self._sportsreference.ImportGamesFromCsv(year, postseason_start_week, game_reader)

    def CalculateRankings(self, year):
        pass
        
    def Display(self):
        seasons = self._repository.AllSeasons()
        print('Total Seasons: ' + str(len(seasons)))
        for season in seasons:
            print()
            print(str(season.year) + ' Season:')
    
            affiliations = self._repository.FindAffiliationsBySeason(season)
            print('Total Teams: ' + str(len(affiliations)))
            print('FBS Teams: ' + str(sum(x.subdivision == Subdivision.FBS for x in affiliations)))
            print('FCS Teams: ' + str(sum(x.subdivision == Subdivision.FCS for x in affiliations)))
    
            games = self._repository.FindGamesBySeason(season)
            print('Total Games: ' + str(len(games)))
