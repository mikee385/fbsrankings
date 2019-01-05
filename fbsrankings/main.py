import csv
import os

from fbsrankings.common import EventBus
from fbsrankings.domain import Factory
from fbsrankings.infrastructure.local import Repository
from fbsrankings.application import Application


data_directory = 'fbsrankings/data'

common_name_map = {}
name_csv_filename = os.path.join(data_directory, 'names.csv')
with open(name_csv_filename, 'r') as name_file:
    name_reader = csv.reader(name_file)
    
    iterrows = iter(name_reader)
    next(iterrows)
    
    for row in iterrows:
        name = row[0].strip()
        alternate_name = row[1].strip()
        
        common_name_map[alternate_name] = name

event_bus = EventBus()
factory = Factory(event_bus)
repository = Repository()
application = Application(factory, repository, common_name_map)

index_csv_filename = os.path.join(data_directory, 'urls.csv')
with open(index_csv_filename, 'r') as index_file:
    index_reader = csv.reader(index_file)
            
    iterrows = iter(index_reader)
    next(iterrows)
    
    for row in iterrows:
        year = int(row[0])
        postseason_start_week = int(row[1])
        team_url = row[2]
        game_url = row[3]
        
        print(str(year) + ': Importing Data')
        
        application.import_sports_reference_season(year, postseason_start_week, team_url, game_url)
        
        print(str(year) + ': Calculating Rankings')
            
        application.calculate_rankings(year)

    application.display()
