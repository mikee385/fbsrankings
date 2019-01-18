import csv
import os

from fbsrankings.common import EventBus
from fbsrankings.infrastructure import TeamNameMap
from fbsrankings.infrastructure.local import UnitOfWork
from fbsrankings.application import Application


data_directory = 'fbsrankings/data'
team_map_filename = os.path.join(data_directory, 'names.csv')
team_name_map = TeamNameMap.from_csv_file(team_map_filename)

event_bus = EventBus()
unit_of_work = UnitOfWork(event_bus)
application = Application(unit_of_work, team_name_map)

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
        
        print(f'{year}: Importing Data')
        
        application.import_season_urls(year, postseason_start_week, team_url, game_url)
        
        print(f'{year}: Calculating Rankings')
            
        application.calculate_rankings(year)

    print()
    application.print_results()
    print()
    application.print_errors()
