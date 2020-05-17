import json

from fbsrankings.application import Application


with open('config_urls.json') as config_file:
    config = json.load(config_file)
application = Application(config)

for year in application.seasons:
    print(f'{year}: Importing Data')
    application.import_season(year)
        
    print(f'{year}: Calculating Rankings')
    application.calculate_rankings(year)

print()
application.print_results()
application.print_errors()
application.print_counts()
print()
