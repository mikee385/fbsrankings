import csv


class TeamNameMap (object):
    def from_csv_file(filename):
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            return TeamNameMap.from_csv_reader(reader)
        
    def from_csv_reader(reader):
        team_name_map = {}
    
        iterrows = iter(reader)
        next(iterrows)
    
        for row in iterrows:
            name = row[0].strip()
            alternate_name = row[1].strip()
        
            team_name_map[alternate_name] = name
            
        return team_name_map
