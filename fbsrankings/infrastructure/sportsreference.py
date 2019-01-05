import csv
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup, Tag

from fbsrankings.domain import SeasonSection, Subdivision, GameStatus, ImportService


class SportsReference (object):
    def __init__(self, import_service):
        if not isinstance(import_service, ImportService):
            raise TypeError('import_service must be of type ImportService')
        self._import_service = import_service
        
        self._common_name_map = {
            'Alabama-Birmingham': 'UAB',
            'Central Florida': 'UCF',
            'Louisiana State': 'LSU',
            'Mississippi': 'Ole Miss',
            'Pittsburgh': 'Pitt',
            'Southern California': 'USC',
            'Southern Methodist': 'SMU',
            'Texas-El Paso': 'UTEP',
            'Texas-San Antonio': 'UTSA'
        }
        
    def import_season_urls(self, year, postseason_start_week, team_url, game_url):
        self.import_team_url(year, team_url)
        self.import_game_url(year, postseason_start_week, game_url)
        
    def import_season_csv_files(self, year, postseason_start_week, team_filename, game_filename):
        self.import_team_csv_file(year, team_filename)
        self.import_game_csv_file(year, postseason_start_week, game_filename)
        
    def import_season_readers(self, year, postseason_start_week, team_reader, game_reader):
        self.import_team_reader(year, team_reader)
        self.import_game_reader(year, postseason_start_week, game_reader)
        
    def import_team_url(self, year, url):
        html = urlopen(url)
        soup = BeautifulSoup(html, "html5lib")
        self.import_team_rows(year, _html_iter(soup))
        
    def import_team_csv_file(self, year, filename):
        with open(filename, 'r') as file:
            self.import_team_reader(year, csv.reader(file))
        
    def import_team_reader(self, year, reader):
        self.import_team_rows(year, iter(reader))
        
    def import_game_url(self, year, postseason_start_week, url):
        html = urlopen(url)
        soup = BeautifulSoup(html, "html5lib")
        self.import_game_rows(year, postseason_start_week, _html_iter(soup))

    def import_game_csv_file(self, year, postseason_start_week, filename):
        with open(filename, 'r') as file:
            self.import_game_reader(year, postseason_start_week, csv.reader(file))
        
    def import_game_reader(self, year, postseason_start_week, reader):
        self.import_game_rows(year, postseason_start_week, iter(reader))

    def import_team_rows(self, year, row_iter):
        season = self._import_service.import_season(year)
        
        header_row = next(row_iter)
        if header_row[0] == '':
            header_row = next(row_iter)
        
        rank_index = header_row.index('Rk')
        name_index = header_row.index('School')

        for row in row_iter:
            if row[rank_index].isdigit():
                name = row[name_index].strip()
                if name in self._common_name_map:
                    name = self._common_name_map[name]
                team = self._import_service.import_team(name)
                self._import_service.import_affiliation(season, team, Subdivision.FBS)
        
    def import_game_rows(self, year, postseason_start_week, row_iter):
        season = self._import_service._repository.find_season_by_year(year)
        if season is None:
            raise ValueError('Teams for season ' + year + 'must be imported before games can be imported')
            
        header_row = next(row_iter)
        if header_row[0] == '':
            header_row = next(row_iter)
            
        rank_index = header_row.index('Rk')
        week_index = header_row.index('Wk')
        date_index = header_row.index('Date')
        notes_index = header_row.index('Notes')
        
        first_team_index = [index for index, column in enumerate(header_row) if column.startswith('Winner')][0]
        
        first_score_index = first_team_index + 1
        
        second_team_index = [index for index, column in enumerate(header_row) if column.startswith('Loser')][0]
        
        second_score_index = second_team_index + 1
        
        home_away_index = first_score_index + 1
        
        for counter, row in enumerate(row_iter):
            if row[rank_index].isdigit():
                week_string = row[week_index].strip()
                date_string = row[date_index].strip()
                first_team_name = row[first_team_index].strip()
                first_score_string = row[first_score_index].strip()
                home_away_symbol = row[home_away_index].strip()
                second_team_name = row[second_team_index].strip()
                second_score_string = row[second_score_index].strip()
                
                week = int(week_string)
                
                try:
                    game_date = datetime.strptime(date_string, '%b %d %Y').date()
                except ValueError:
                    game_date = datetime.strptime(date_string, '%b %d, %Y').date()
                
                if (first_team_name.startswith('(')):
                    start = first_team_name.find(')')
                    first_team_name = first_team_name[start + 2:].strip()
                
                if first_team_name in self._common_name_map:
                    first_team_name = self._common_name_map[first_team_name]
                
                if first_score_string == '':
                    first_score = None
                else:
                    first_score = int(first_score_string)
                    
                if (second_team_name.startswith('(')):
                    start = second_team_name.find(')')
                    second_team_name = second_team_name[start + 2:].strip()
                    
                if second_team_name in self._common_name_map:
                    second_team_name = self._common_name_map[second_team_name]
                    
                if second_score_string == '':
                    second_score = None
                else:
                    second_score = int(second_score_string)
                
                if home_away_symbol == '':
                    home_team_name = first_team_name
                    home_team_score = first_score
                    away_team_name = second_team_name
                    away_team_score = second_score
                elif home_away_symbol == '@':
                    away_team_name = first_team_name
                    away_team_score = first_score
                    home_team_name = second_team_name
                    home_team_score = second_score
                else:
                    raise ValueError(
                        'Unable to convert symbol "' + home_away_symbol + '" to an "@" on line ' + str(counter))
                        
                home_team = self._import_service.import_team(home_team_name)
                self._import_service.import_affiliation(season, home_team, Subdivision.FCS)
                
                away_team = self._import_service.import_team(away_team_name)
                self._import_service.import_affiliation(season, away_team, Subdivision.FCS)
                
                notes = row[notes_index]
                
                if (week >= postseason_start_week):
                    season_section = SeasonSection.POSTSEASON
                elif 'Championship' in notes:
                    season_section = SeasonSection.CONFERENCE_CHAMPIONSHIP
                else:
                    season_section = SeasonSection.REGULAR_SEASON
                    
                game = self._import_service.import_game(season, week, game_date, season_section, home_team, away_team)
                
                if home_team_score is not None and away_team_score is not None and game.status != GameStatus.COMPLETED:
                    game.complete(home_team_score, away_team_score)
                    

def _html_iter(soup):
    row_iter = iter(soup.find_all('tr'))
    for row in row_iter:
        yield [child.getText() for child in filter(lambda c: isinstance(c, Tag), row.children)]
