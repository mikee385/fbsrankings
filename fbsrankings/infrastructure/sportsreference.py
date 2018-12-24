from datetime import datetime
from fbsrankings.domain.season import SeasonRepository, SeasonSection
from fbsrankings.domain.team import TeamRepository
from fbsrankings.domain.affiliation import AffiliationRepository, Subdivision
from fbsrankings.domain.game import GameRepository


class SportsReference (object):
    def __init__(self, repository):
        if not isinstance(repository, SeasonRepository):
            raise TypeError('repository must be of type SeasonRepository')
        if not isinstance(repository, TeamRepository):
            raise TypeError('repository must be of type TeamRepository')
        if not isinstance(repository, AffiliationRepository):
            raise TypeError('repository must be of type AffiliationRepository')
        if not isinstance(repository, GameRepository):
            raise TypeError('repository must be of type GameRepository')
        self._repository = repository
        
    def ImportTeamsFromCsv(self, year, csv_reader):
        season = self._ImportSeason(year)
        
        iterrows = iter(csv_reader)
        row = next(iterrows)
        if row[0] == '':
            row = next(iterrows)
        
        rank_index = row.index('Rk')
        name_index = row.index('School')

        for row in iterrows:
            if row[rank_index].isdigit():
                name = row[name_index]
                self._ImportTeam(season, name, Subdivision.FBS)
                
    def ImportGamesFromCsv(self, year, postseason_start_week, csv_reader):
        season = self._repository.FindSeasonByYear(year)
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
                        
                home_team = self._ImportTeam(season, home_team_name, Subdivision.FCS)
                
                away_team = self._ImportTeam(season, away_team_name, Subdivision.FCS)
                
                if (week >= postseason_start_week):
                    season_section = SeasonSection.POSTSEASON
                else:
                    season_section = SeasonSection.REGULAR_SEASON
                    
                self._ImportGame(season, week, game_date, season_section, home_team, away_team, home_team_score, away_team_score)
                
    def _ImportSeason(self, year):
        season = self._repository.FindSeasonByYear(year)
        if season is None:
            season = self._repository.AddSeason(year)
            
        return season
                
    def _ImportTeam(self, season, name, subdivision):
        team = self._repository.FindTeamByName(name)
        if team is None:
            team = self._repository.AddTeam(name)
            self._repository.AddAffiliation(season, team, subdivision)
        else:
            affiliation = self._repository.FindAffiliationBySeasonTeam(season, team)
            if affiliation is None:
                self._repository.AddAffiliation(season, team, subdivision)
        
        return team
        
    def _ImportGame(self, *args, **kwargs):
        self._repository.AddGame(*args, **kwargs)
