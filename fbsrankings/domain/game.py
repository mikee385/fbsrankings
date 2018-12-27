from datetime import date

from fbsrankings.common.identifier import Identifier
from fbsrankings.common.event import Event, EventBus
from fbsrankings.domain.season import Season, SeasonID, SeasonSection
from fbsrankings.domain.team import Team, TeamID


class GameID (Identifier):
    pass


class Game (object):
    def __init__(self, event_bus, ID, season, week, date_, season_section, home_team, away_team, home_team_score=None, away_team_score=None):
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._event_bus = event_bus
        
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
        
        if not isinstance(season_section, SeasonSection):
            raise TypeError('season_section must be of type SeasonSection')
        self.season_section = season_section
        
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
             
        if home_team_score is not None and away_team_score is not None:
            self._set_score(home_team_score, away_team_score)
        else:
            self.winning_team_ID = None
            self.winning_team_score = None
            self.losing_team_ID = None
            self.losing_team_score = None
            
    def schedule(*args, **kwargs):
        game = Game(*args, **kwargs)
        game._event_bus.raise_event(GameScheduledEvent(*args, **kwargs))
        
        return game
        
    def reschedule(self, week, date_):
        old_week = self.week
        old_date = self.date
        
        if not isinstance(week, int):
            raise TypeError('week must be of type int')
        self.week = week
            
        if not isinstance(date_, date):
            raise TypeError('date_ must be of type date')
        self.date = date_
        
        self._event_bus.raise_event(GameRescheduledEvent(self.ID, old_week, old_date, week, date_))
        
    def cancel(self):
        self._event_bus.raise_event(GameCanceledEvent(self.ID))
        
    def complete(self, home_team_score, away_team_score):
        if home_team_score is None:
            raise ValueError('home_team_score cannot be None')
        if away_team_score is None:
            raise ValueError('away_team_score cannot be None')
        self._set_score(home_team_score, away_team_score)
        
        self._event_bus.raise_event(GameCompletedEvent(self.ID, home_team_score, away_team_score))
        
    def _set_score(self, home_team_score, away_team_score):
        if not isinstance(home_team_score, int):
            raise TypeError('home_team_score must be of type int')
        self.home_team_score = home_team_score
            
        if not isinstance(away_team_score, int):
            raise TypeError('away_team_score must be of type int')
        self.away_team_score = away_team_score
            
        if home_team_score > away_team_score:
            self.winning_team_ID = self.home_team_ID
            self.winning_team_score = self.home_team_score
            self.losing_team_ID = self.away_team_ID
            self.losing_team_score = self.away_team_score
        elif away_team_score > home_team_score:
            self.winning_team_ID = self.away_team_ID
            self.winning_team_score = self.away_team_score
            self.losing_team_ID = self.home_team_ID
            self.losing_team_score = self.home_team_score
        else:
            self.winning_team_ID = None
            self.winning_team_score = None
            self.losing_team_ID = None
            self.losing_team_score = None


class GameRepository (object):
    def add_game(self, *args, **kwargs):
        pass

    def find_game(self, ID):
        pass
        
    def all_games(self):
        pass


class GameScheduledEvent (Event):
    def __init__(self, ID, season_ID, week, date_, season_section, home_team_ID, away_team_ID):
        self.ID = ID
        self.season_ID = season_ID
        self.week = week
        self.date = date_
        self.season_section = season_section
        self.home_team_ID = home_team_ID
        self.away_team_ID = away_team_ID
    

class GameRescheduledEvent (Event):
    def __init__(self, ID, old_week, old_date, week, date_):
        self.ID = ID
        self.old_week = old_week
        self.old_date = old_date
        self.week = week
        self.date = date_
    

class GameCanceledEvent (Event):
    def __init__(self, ID):
        self.ID = ID
    

class GameCompletedEvent (Event):
    def __init__(self, ID, home_team_score, away_team_score):
        self.ID = ID
        self.home_team_score = home_team_score
        self.away_team_score = away_team_score
