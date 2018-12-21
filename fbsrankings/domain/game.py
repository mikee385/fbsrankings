from datetime import date
from fbsrankings.common.identifier import Identifier
from fbsrankings.domain.season import Season, SeasonID, SeasonSection
from fbsrankings.domain.team import Team, TeamID


class GameID (Identifier):
    pass


class Game (object):
    def __init__(self, ID, season, week, date_, home_team, away_team, season_section):
        if not isinstance(ID, GameID):
            raise TypeError('ID must be of type GameID')
        self.ID = ID
        
        if isinstance(season, Season):
            self.season_ID = season.ID
        elif isinstance(season, SeasonID):
            self.season_ID = season
        else:
            raise TypeError('season must be of type Season or SeasonID')
            
        if not isinstance(week, int):
            raise TypeError('week must be of type int')
        self.week = week
            
        if not isinstance(date_, date):
            raise TypeError('date_ must be of type date')
        self.date = date_
        
        if isinstance(home_team, Team):
            self.home_team_ID = home_team.ID
        elif isinstance(home_team, TeamID):
            self.home_team_ID = home_team
        else:
            raise TypeError('home_team must be of type Team or TeamID')
        
        if isinstance(away_team, Team):
            self.away_team_ID = away_team.ID
        elif isinstance(away_team, TeamID):
            self.away_team_ID = away_team
        else:
            raise TypeError('away_team must be of type Team or TeamID')
            
        if not isinstance(season_section, SeasonSection):
            raise TypeError('season_section must be of type SeasonSection')
        self.season_section = season_section


class GameRepository (object):
    def AddGame(self, *args, **kwargs):
        pass

    def FindGame(self, ID):
        pass
        
    def AllGames(self):
        pass
        