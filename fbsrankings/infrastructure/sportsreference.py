from datetime import datetime

from fbsrankings.domain.season import SeasonSection
from fbsrankings.domain.affiliation import Subdivision
from fbsrankings.domain.importservice import ImportService


class SportsReference (object):
    def __init__(self, import_service):
        if not isinstance(import_service, ImportService):
            raise TypeError('import_service must be of type ImportService')
        self._import_service = import_service
        
    def import_teams_from_csv(self, year, csv_reader):
        season = self._import_service.import_season(year)
        
        iterrows = iter(csv_reader)
        row = next(iterrows)
        if row[0] == '':
            row = next(iterrows)
        
        rank_index = row.index('Rk')
        name_index = row.index('School')

        for row in iterrows:
            if row[rank_index].isdigit():
                name = row[name_index]
                team = self._import_service.import_team(name)
                self._import_service.import_affiliation(season, team, Subdivision.FBS)
                
    def import_games_from_csv(self, year, postseason_start_week, csv_reader):
        season = self._import_service._repository.find_season_by_year(year)
        if season is None:
            raise ValueError('Teams for season ' + year + 'must be imported before games can be imported')
            
        iterrows = iter(csv_reader)
        row = next(iterrows)
        if row[0] == '':
            row = next(iterrows)
            
        rank_index = row.index('Rk')
        week_index = row.index('Wk')
        date_index = row.index('Date')
        
        first_team_index = [index for index, column in enumerate(row) if column.startswith('Winner')][0]
        
        first_score_index = first_team_index + 1
        
        second_team_index = [index for index, column in enumerate(row) if column.startswith('Loser')][0]
        
        second_score_index = second_team_index + 1
        
        home_away_index = first_score_index + 1
        
        for counter, row in enumerate(csv_reader):
            if row[rank_index].isdigit():
                week_string = row[week_index]
                date_string = row[date_index]
                first_team_name = row[first_team_index]
                first_score_string = row[first_score_index]
                home_away_symbol = row[home_away_index]
                second_team_name = row[second_team_index]
                second_score_string = row[second_score_index]
                
                week = int(week_string)
                
                game_date = datetime.strptime(date_string, '%b %d %Y').date()
                
                if (first_team_name.startswith('(')):
                    start = first_team_name.find(')')
                    first_team_name = first_team_name[start + 2:]
                
                if first_score_string == '':
                    first_score = None
                else:
                    first_score = int(first_score_string)
                    
                if (second_team_name.startswith('(')):
                    start = second_team_name.find(')')
                    second_team_name = second_team_name[start + 2:]
                    
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
                
                if (week >= postseason_start_week):
                    season_section = SeasonSection.POSTSEASON
                else:
                    season_section = SeasonSection.REGULAR_SEASON
                    
                game = self._import_service.import_game(season, week, game_date, season_section, home_team, away_team)
                
                if home_team_score is not None and away_team_score is not None:
                    game.complete(home_team_score, away_team_score)
