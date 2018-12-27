import csv
import os

from fbsrankings.common.event import EventBus
from fbsrankings.infrastructure.local.repository import Repository
from fbsrankings.application import Application


event_bus = EventBus()
repository = Repository(event_bus)
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
        application.import_sports_reference_season(year, postseason_start_week, team_csv_filename, game_csv_filename)
            
        application.calculate_rankings(year)
    
    application.display()
