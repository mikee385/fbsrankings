import csv
import os
from fbsrankings.infrastructure.local.repository import Repository
from fbsrankings.application import Application

repository = Repository()
application = Application(repository)

data_directory = 'fbsrankings/data'
index_csv_filename = os.path.join(data_directory, 'index.csv')
with open(index_csv_filename, 'r') as index_file:
    index_reader = csv.reader(index_file)
            
    iterrows = iter(index_reader)
    next(iterrows)
    
    for row in iterrows:
        year = int(row[0])
        postseason_start_week = int(row[1])
        team_csv_filename = os.path.join(data_directory, row[2])
        game_csv_filename = os.path.join(data_directory, row[3])

        with open(team_csv_filename, 'r') as team_file:
            team_reader = csv.reader(team_file)
            application.ImportTeamsFromCsv(year, team_reader)
            
        with open(game_csv_filename, 'r') as game_file:
            game_reader = csv.reader(game_file)
            application.ImportGamesFromCsv(year, postseason_start_week, game_reader)
            
        application.CalculateRankings(year)
    
    application.Display()
