import csv
import os
import sqlite3

from fbsrankings.infrastructure import TeamNameMap
from fbsrankings.infrastructure.sqlite import UnitOfWorkFactory
from fbsrankings.application import Application


data_directory = 'fbsrankings/data'
team_map_filename = os.path.join(data_directory, 'names.csv')
team_name_map = TeamNameMap.from_csv_file(team_map_filename)

db_filename = os.path.join(data_directory, 'fbsrankings.db')
connection = sqlite3.connect(db_filename)
try:
    connection.execute('PRAGMA foreign_keys = ON')
    
    uow_factory = UnitOfWorkFactory(connection)
    application = Application(uow_factory, team_name_map)

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
        application.print_errors()

finally:
    connection.close()
