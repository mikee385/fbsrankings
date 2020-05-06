import csv
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup, Tag

from fbsrankings.domain import SeasonSection, Subdivision, GameStatus, ImportService, ValidationService, CancelService


class SeasonSource:
    def __init__(self, postseason_start_week, source_type, team_source, game_source):
        self.postseason_start_week = postseason_start_week
        self.source_type = source_type
        self.team_source = team_source
        self.game_source = game_source


class SportsReference (object):
    def __init__(self, alternate_names):        
        if alternate_names is not None:
            self._alternate_names = alternate_names
        else:
            self._alternate_names = {}

        self._season_sources = {}

    def add_season_source(self, year, postseason_start_week, source_type, team_source, game_source):
        self._season_sources[year] = SeasonSource(postseason_start_week, source_type, team_source, game_source)

    def import_season(self, year, import_service, validation_service, cancel_service):
        if not isinstance(import_service, ImportService):
            raise TypeError('import_service must be of type ImportService')
        
        if validation_service is not None and not isinstance(validation_service, ValidationService):
            raise TypeError('validation_service must be of type ValidationService')
        
        if cancel_service is not None and not isinstance(cancel_service, CancelService):
            raise TypeError('cancel_service must be of type CancelService')

        season_source = self._season_sources.get(year)
        if season_source is None:
            raise ValueError(f'Season data is not available for {year}')

        if season_source.source_type == 'CSV':
            self._import_season_from_csv_files(year, season_source.postseason_start_week, season_source.team_source, season_source.game_source, import_service, validation_service)
        elif season_source.source_type == 'URL':
            self._import_season_from_urls(year, season_source.postseason_start_week, season_source.team_source, season_source.game_source, import_service, validation_service)
        else:
            raise ValueError(f'Unknown source type: {season_source.source_type}')
        
        if cancel_service is not None:
            cancel_service.cancel_past_games(import_service.games)
        
    def _import_season_from_urls(self, year, postseason_start_week, team_url, game_url, import_service, validation_service):
        self._import_teams_from_url(year, team_url, import_service, validation_service)
        self._import_games_from_url(year, postseason_start_week, game_url, import_service, validation_service)
        
    def _import_season_from_csv_files(self, year, postseason_start_week, team_filename, game_filename, import_service, validation_service):
        self._import_teams_from_csv_file(year, team_filename, import_service, validation_service)
        self._import_games_from_csv_file(year, postseason_start_week, game_filename, import_service, validation_service)
        
    def _import_season_from_readers(self, year, postseason_start_week, team_reader, game_reader, import_service, validation_service):
        self._import_teams_from_reader(year, team_reader, import_service, validation_service)
        self._import_games_from_reader(year, postseason_start_week, game_reader, import_service, validation_service)
        
    def _import_teams_from_url(self, year, url, import_service, validation_service):
        html = urlopen(url)
        soup = BeautifulSoup(html, "html5lib")
        self._import_teams_from_rows(year, _html_iter(soup), import_service, validation_service)
        
    def _import_teams_from_csv_file(self, year, filename, import_service, validation_service):
        with open(filename, 'r') as file:
            self._import_teams_from_reader(year, csv.reader(file), import_service, validation_service)
        
    def _import_teams_from_reader(self, year, reader):
        self._import_teams_from_rows(year, iter(reader), import_service, validation_service)
        
    def _import_games_from_url(self, year, postseason_start_week, url, import_service, validation_service):
        html = urlopen(url)
        soup = BeautifulSoup(html, "html5lib")
        self._import_games_from_rows(year, postseason_start_week, _html_iter(soup), import_service, validation_service)

    def _import_games_from_csv_file(self, year, postseason_start_week, filename, import_service, validation_service):
        with open(filename, 'r') as file:
            self._import_games_from_reader(year, postseason_start_week, csv.reader(file), import_service, validation_service)
        
    def _import_games_from_reader(self, year, postseason_start_week, reader, import_service, validation_service):
        self._import_games_from_rows(year, postseason_start_week, iter(reader), import_service, validation_service)

    def _import_teams_from_rows(self, year, row_iter, import_service, validation_service):
        season = import_service.import_season(year)
        if validation_service is not None:
            validation_service.validate_season_data(season, year)
        
        header_row = next(row_iter)
        if header_row[0] == '':
            header_row = next(row_iter)
        
        rank_index = header_row.index('Rk')
        name_index = header_row.index('School')

        for row in row_iter:
            if row[rank_index].isdigit():
                name = row[name_index].strip()
                if name in self._alternate_names:
                    name = self._alternate_names[name]
                team = import_service.import_team(name)
                affiliation = import_service.import_affiliation(season.ID, team.ID, Subdivision.FBS)
                
                if validation_service is not None:
                    validation_service.validate_team_data(team, name)
                    validation_service.validate_affiliation_data(affiliation, season.ID, team.ID, affiliation.subdivision)
        
    def _import_games_from_rows(self, year, postseason_start_week, row_iter, import_service, validation_service):
        season = next((s for s in import_service.seasons if s.year == year), None)
        if season is None:
            season = import_service._season_repository.find_by_year(year)
            if season is None:
                raise ValueError(f'Teams for season {year} must be imported before games can be imported')
            
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
                        
                home_team = import_service.import_team(home_team_name)
                home_team_affiliation = import_service.import_affiliation(season.ID, home_team.ID, Subdivision.FCS)
                
                away_team = import_service.import_team(away_team_name)
                away_team_affiliation = import_service.import_affiliation(season.ID, away_team.ID, Subdivision.FCS)
                
                if validation_service is not None:
                    validation_service.validate_team_data(home_team, home_team_name)
                    validation_service.validate_affiliation_data(home_team_affiliation, season.ID, home_team.ID, home_team_affiliation.subdivision)
                    
                    validation_service.validate_team_data(away_team, away_team_name)
                    validation_service.validate_affiliation_data(away_team_affiliation, season.ID, away_team.ID, away_team_affiliation.subdivision)
                
                notes = row[notes_index].strip()
                
                if (week >= postseason_start_week):
                    season_section = SeasonSection.POSTSEASON
                else:
                    season_section = SeasonSection.REGULAR_SEASON
                    
                game = import_service.import_game(season.ID, week, date_, season_section, home_team.ID, away_team.ID, notes)
                
                if home_team_score is not None and away_team_score is not None and game.status != GameStatus.COMPLETED:
                    game.complete(home_team_score, away_team_score)
                
                if game.notes != notes:
                    game.update_notes(notes)
                
                if validation_service is not None:
                    validation_service.validate_game_data(game, season.ID, week, date_, season_section, home_team.ID, away_team.ID, home_team_score, away_team_score, game.status, notes)
        
        if validation_service is not None:
            affiliations = [a for a in import_service.affiliations if a.season_ID == season.ID]
            if len(affiliations) == 0:
                affiliations = import_service._affiliation_repository.find_by_season(season)
                
            games = [g for g in import_service.games if g.season_ID == season.ID]
            if len(games) == 0:
                games = import_service._game_repository.find_by_season(season)
            validation_service.validate_games(affiliations, games)


def _html_iter(soup):
    row_iter = iter(soup.find_all('tr'))
    for row in row_iter:
        yield [child.getText() for child in filter(lambda c: isinstance(c, Tag), row.children)]
