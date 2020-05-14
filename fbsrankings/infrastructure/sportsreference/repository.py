import csv
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup, Tag

from fbsrankings.common import EventBus, ReadOnlyEventBus
from fbsrankings.domain import Repository as BaseRepository, SeasonSection, Subdivision, GameStatus
from fbsrankings.infrastructure.memory import DataStore as MemoryDataStore
from fbsrankings.infrastructure.sportsreference import SeasonRepository, TeamRepository, AffiliationRepository, GameRepository


class SeasonSource (object):
    def __init__(self, ID, year, postseason_start_week, source_type, team_source, game_source):
        self.ID = ID
        self.year = year
        self.postseason_start_week = postseason_start_week
        
        self.source_type = source_type
        self.team_source = team_source
        self.game_source = game_source
        
        self.is_loaded = False


class Repository (BaseRepository):
    def __init__(self, alternate_names):
        self._cache = MemoryDataStore()
        self._repository = self._cache.unit_of_work(ReadOnlyEventBus()).repository
        
        self._sources_by_year = {}
        self._sources_by_ID = {}
        
        if alternate_names is not None:
            self._alternate_names = alternate_names
        else:
            self._alternate_names = {}
            
        super().__init__(
            SeasonRepository(self, self._repository.season),
            TeamRepository(self, self._repository.team),
            AffiliationRepository(self, self._repository.affiliation),
            GameRepository(self, self._repository.game)
        )
        
    def add_source(self, year, postseason_start_week, source_type, team_source, game_source):
        if self._sources_by_year.get(year) is not None:
            raise ValueError(f'Source already exists for year {year}')
            
        unit_of_work = self._cache.unit_of_work(EventBus())
        season = unit_of_work.factory.season.register(year)
        unit_of_work.commit()
            
        source = SeasonSource(season.ID, year, postseason_start_week, source_type, team_source, game_source)
        self._sources_by_year[year] = source
        self._sources_by_ID[season.ID] = source
        
    def load_from_source(self, year):
        self._load_by_year(year)
        
    def load_all(self):
        for source in self._sources_by_year.values():
            self._load_from_source(source)
        
    def _load_by_year(self, year):
        source = self._sources_by_year.get(year)
        if source is None:
            raise ValueError(f'Source has not been added for year {year}')
        self._load_from_source(source)
        
    def _load_by_ID(self, ID):
        source = self._sources_by_ID.get(ID)
        if source is None:
            raise ValueError(f'Source has not been added for ID {ID}')
        self._load_from_source(source)
        
    def _load_from_source(self, source):
        if source.is_loaded:
            return
        
        if source.source_type == 'CSV':
            self._load_from_csv(source)
        elif source.source_type == 'URL':
            self._load_from_url(source)
        else:
            raise ValueError(f'Unknown source type: {source.source_type}')
        
    def _load_from_csv(self, source):
        with open(source.team_source, 'r') as team_file, open(source.game_source, 'r') as game_file:
            team_rows = iter(csv.reader(team_file))
            game_rows = iter(csv.reader(game_file))
            self._load_from_rows(source, team_rows, game_rows)
        
    def _load_from_url(self, source):
        team_html = urlopen(source.team_source)
        team_soup = BeautifulSoup(team_html, "html5lib")
        team_rows = _html_iter(team_soup)
        
        game_html = urlopen(source.game_source)
        game_soup = BeautifulSoup(game_html, "html5lib")
        game_rows = _html_iter(game_soup)
        
        self._load_from_rows(source, team_rows, game_rows)
        
    def _load_from_rows(self, source, team_rows, game_rows):
        unit_of_work = self._cache.unit_of_work(EventBus())
        
        fbs_teams = {}
        fcs_teams = {}
        
        header_row = next(team_rows)
        if header_row[0] == '':
            header_row = next(team_rows)
        
        rank_index = header_row.index('Rk')
        name_index = header_row.index('School')

        for row in team_rows:
            if row[rank_index].isdigit():
                name = row[name_index].strip()
                if name in self._alternate_names:
                    name = self._alternate_names[name]
                team = unit_of_work.repository.team.find_by_name(name)
                if team is None:
                    team = unit_of_work.factory.team.register(name)
                unit_of_work.factory.affiliation.register(source.ID, team.ID, Subdivision.FBS)
                fbs_teams[name] = team
                
        games = []
        
        header_row = next(game_rows)
        if header_row[0] == '':
            header_row = next(game_rows)
            
        rank_index = header_row.index('Rk')
        week_index = header_row.index('Wk')
        date_index = header_row.index('Date')
        notes_index = header_row.index('Notes')
        
        first_team_index = [index for index, column in enumerate(header_row) if column.startswith('Winner')][0]
        
        first_score_index = first_team_index + 1
        
        second_team_index = [index for index, column in enumerate(header_row) if column.startswith('Loser')][0]
        
        second_score_index = second_team_index + 1
        
        home_away_index = first_score_index + 1
        
        for counter, row in enumerate(game_rows):
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
                    date_ = datetime.strptime(date_string, '%b %d %Y').date()
                except ValueError:
                    date_ = datetime.strptime(date_string, '%b %d, %Y').date()
                
                if (first_team_name.startswith('(')):
                    start = first_team_name.find(')')
                    first_team_name = first_team_name[start + 2:].strip()
                
                if first_team_name in self._alternate_names:
                    first_team_name = self._alternate_names[first_team_name]
                
                if first_score_string == '':
                    first_score = None
                else:
                    first_score = int(first_score_string)
                    
                if (second_team_name.startswith('(')):
                    start = second_team_name.find(')')
                    second_team_name = second_team_name[start + 2:].strip()
                    
                if second_team_name in self._alternate_names:
                    second_team_name = self._alternate_names[second_team_name]
                    
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
                    raise ValueError(f'Unable to convert symbol "{home_away_symbol}" to an "@" on line {counter}')
                    
                home_team = fbs_teams.get(home_team_name)
                if home_team is None:
                    home_team = fcs_teams.get(home_team_name)
                    if home_team is None:
                        home_team = unit_of_work.repository.team.find_by_name(home_team_name)
                        if home_team is None:
                            home_team = unit_of_work.factory.team.register(home_team_name)
                        unit_of_work.factory.affiliation.register(source.ID, home_team.ID, Subdivision.FCS)
                        fcs_teams[home_team_name] = home_team
                
                away_team = fbs_teams.get(away_team_name)
                if away_team is None:
                    away_team = fcs_teams.get(away_team_name)
                    if away_team is None:
                        away_team = unit_of_work.repository.team.find_by_name(away_team_name)
                        if away_team is None:
                            away_team = unit_of_work.factory.team.register(away_team_name)
                        unit_of_work.factory.affiliation.register(source.ID, away_team.ID, Subdivision.FCS)
                        fcs_teams[away_team_name] = away_team
                
                notes = row[notes_index].strip()
                
                if (week >= source.postseason_start_week):
                    season_section = SeasonSection.POSTSEASON
                else:
                    season_section = SeasonSection.REGULAR_SEASON
                    
                game = unit_of_work.factory.game.schedule(source.ID, week, date_, season_section, home_team.ID, away_team.ID, notes)
                games.append(game)
                
                if home_team_score is not None and away_team_score is not None and game.status != GameStatus.COMPLETED:
                    game.complete(home_team_score, away_team_score)
                
                if game.notes != notes:
                    game.update_notes(notes)
        
        most_recent_completed_week = 0
        for game in games:
            if game.status == GameStatus.COMPLETED:
                if game.week > most_recent_completed_week:
                    most_recent_completed_week = game.week
        for game in games:
            if game.status == GameStatus.SCHEDULED:
                if game.week < most_recent_completed_week:
                    game.cancel()
                    
        unit_of_work.commit()
        source.is_loaded = True
        

def _html_iter(soup):
    row_iter = iter(soup.find_all('tr'))
    for row in row_iter:
        yield [child.getText() for child in filter(lambda c: isinstance(c, Tag), row.children)]
