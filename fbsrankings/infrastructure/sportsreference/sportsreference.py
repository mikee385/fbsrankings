import csv
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup, Tag

from fbsrankings.domain import SeasonSection, Subdivision, GameStatus


class SeasonSource (object):
    def __init__(self, year, postseason_start_week, source_type, team_source, game_source):
        self.year = year
        self.postseason_start_week = postseason_start_week
        
        self.source_type = source_type
        self.team_source = team_source
        self.game_source = game_source


class SportsReference (object):
    def __init__(self, alternate_names, validation_service):
        self._sources = {}
        
        if alternate_names is not None:
            self._alternate_names = alternate_names
        else:
            self._alternate_names = {}
            
        self._validation_service = validation_service
        
    def add_source(self, year, postseason_start_week, source_type, team_source, game_source):
        if self._sources.get(year) is not None:
            raise ValueError(f'Source already exists for year {year}')
        
        self._sources[year] = SeasonSource(year, postseason_start_week, source_type, team_source, game_source)
        
    def import_season(self, year, repository):
        source = self._sources.get(year)
        if source is None:
            raise ValueError(f'Source has not been added for year {year}')
        
        if source.source_type == 'CSV':
            self._import_from_csv(source, repository)
        elif source.source_type == 'URL':
            self._import_from_url(source, repository)
        else:
            raise ValueError(f'Unknown source type: {source.source_type}')
        
    def _import_from_csv(self, source, repository):
        with open(source.team_source, 'r') as team_file, open(source.game_source, 'r') as game_file:
            team_rows = iter(csv.reader(team_file))
            game_rows = iter(csv.reader(game_file))
            self._import_from_rows(source, team_rows, game_rows, repository)
        
    def _import_from_url(self, source, repository):
        team_html = urlopen(source.team_source)
        team_soup = BeautifulSoup(team_html, "html5lib")
        team_rows = _html_iter(team_soup)
        
        game_html = urlopen(source.game_source)
        game_soup = BeautifulSoup(game_html, "html5lib")
        game_rows = _html_iter(game_soup)
        
        self._import_from_rows(source, team_rows, game_rows, repository)
        
    def _import_from_rows(self, source, team_rows, game_rows, repository):
        teams = {}
        affiliations = {}
        games = {}
        
        season = self._import_season(repository, source.year)
        
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
                team = self._import_team(repository, teams, name)
                self._import_affiliation(repository, affiliations, season.ID, team.ID, Subdivision.FBS)
        
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
                    
                home_team = self._import_team(repository, teams, home_team_name)
                    
                self._import_affiliation(repository, affiliations, season.ID, home_team.ID, Subdivision.FCS)
                
                away_team = self._import_team(repository, teams, away_team_name)
                self._import_affiliation(repository, affiliations, season.ID, away_team.ID, Subdivision.FCS)

                notes = row[notes_index].strip()
                
                if (week >= source.postseason_start_week):
                    season_section = SeasonSection.POSTSEASON
                else:
                    season_section = SeasonSection.REGULAR_SEASON
                    
                game = self._import_game(repository, games, season.ID, week, date_, season_section, home_team.ID, away_team.ID, home_team_score, away_team_score, notes)
        
        most_recent_completed_week = 0
        for game in games.values():
            if game.status == GameStatus.COMPLETED:
                if game.week > most_recent_completed_week:
                    most_recent_completed_week = game.week
        for game in games.values():
            if game.status == GameStatus.SCHEDULED:
                if game.week < most_recent_completed_week:
                    game.cancel()
                    
        if self._validation_service is not None:
            self._validation_service.validate_season_games(affiliations.values(), games.values())
                    
    def _import_season(self, repository, year):
        season = repository.season.find_by_year(year)
        if season is None:
            season = repository.season.register(year)
            
        if self._validation_service is not None:
            self._validation_service.validate_season_data(season, year)
            
        return season
        
    def _import_team(self, repository, cache, name):
        key = name
        
        team = cache.get(key)
        if team is None:
            team = repository.team.find_by_name(name)
            if team is None:
                team = repository.team.register(name)
            cache[key] = team
            
        if self._validation_service is not None:
            self._validation_service.validate_team_data(team, name)
            
        return team
        
    def _import_affiliation(self, repository, cache, season_ID, team_ID, subdivision):
        key = (season_ID, team_ID)
        
        affiliation = cache.get(key)
        if affiliation is None:
            affiliation = repository.affiliation.find_by_season_team(season_ID, team_ID)
            if affiliation is None:
                affiliation = repository.affiliation.register(season_ID, team_ID, subdivision)
            cache[key] = affiliation
            
        if self._validation_service is not None:
            self._validation_service.validate_affiliation_data(affiliation, season_ID, team_ID, affiliation.subdivision)
            
        return affiliation
        
    def _import_game(self, repository, cache, season_ID, week, date_, season_section, home_team_ID, away_team_ID, home_team_score, away_team_score, notes):
        if home_team_ID < away_team_ID:
            key = (season_ID, week, home_team_ID, away_team_ID)
        else:
            key = (season_ID, week, away_team_ID, home_team_ID)
            
        game = cache.get(key)
        if game is None:
            game = repository.game.find_by_season_teams(season_ID, week, home_team_ID, away_team_ID)
            if game is None:
                game = repository.game.schedule(season_ID, week, date_, season_section, home_team_ID, away_team_ID, notes)
            cache[key] = game
        
        if date_ != game.date:
            game.reschedule(week, date_)
            
        if home_team_score is not None and away_team_score is not None and game.status != GameStatus.COMPLETED:
            game.complete(home_team_score, away_team_score)
                
        if notes != game.notes:
            game.update_notes(notes)
            
        if self._validation_service is not None:
            self._validation_service.validate_game_data(game, season_ID, week, date_, season_section, home_team_ID, away_team_ID, home_team_score, away_team_score, game.status, notes)
            
        return game
        

def _html_iter(soup):
    row_iter = iter(soup.find_all('tr'))
    for row in row_iter:
        yield [child.getText() for child in filter(lambda c: isinstance(c, Tag), row.children)]