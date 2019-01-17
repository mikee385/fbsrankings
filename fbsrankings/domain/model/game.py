from uuid import uuid4
from enum import Enum
from datetime import date

from fbsrankings.common import Identifier, Event, EventBus
from fbsrankings.domain import Season, SeasonID, SeasonSection, Team, TeamID


class GameStatus (Enum):
    SCHEDULED = 0
    COMPLETED = 1
    CANCELED = 2


class GameID (Identifier):
    pass
    

class GameStatusError (Exception):
    def __init__(self, message, game_ID, status):
        super().__init__(message)
        self.game_ID = game_ID
        self.status = status


class Game (object):
    def __init__(self, event_bus, ID, season, week, date_, season_section, home_team, away_team, home_team_score, away_team_score, status, notes):
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._event_bus = event_bus
        
        if not isinstance(ID, GameID):
            raise TypeError('ID must be of type GameID')
        self._ID = ID
        
        if isinstance(season, Season):
            self._season_ID = season.ID
        elif isinstance(season, SeasonID):
            self._season_ID = season
        else:
            raise TypeError('season must be of type Season or SeasonID')
            
        if not isinstance(week, int):
            raise TypeError('week must be of type int')
        self._week = week
            
        if not isinstance(date_, date):
            raise TypeError('date_ must be of type date')
        self._date = date_
        
        if not isinstance(season_section, SeasonSection):
            raise TypeError('season_section must be of type SeasonSection')
        self._season_section = season_section
        
        if isinstance(home_team, Team):
            self._home_team_ID = home_team.ID
        elif isinstance(home_team, TeamID):
            self._home_team_ID = home_team
        else:
            raise TypeError('home_team must be of type Team or TeamID')
        
        if isinstance(away_team, Team):
            self._away_team_ID = away_team.ID
        elif isinstance(away_team, TeamID):
            self._away_team_ID = away_team
        else:
            raise TypeError('away_team must be of type Team or TeamID')
            
        if home_team_score is not None and away_team_score is not None:
            if status != GameStatus.COMPLETED:
                raise ValueError('Game must be COMPLETED in order to have scores')
            
            self._set_score(home_team_score, away_team_score)

        elif home_team_score is not None:
            raise ValueError('Home team score must be None if away team score is None')

        elif away_team_score is not None:
            raise ValueError('Away team score must be None if home team score is None')

        elif status == GameStatus.COMPLETED:
                raise ValueError('Game must be have scores in order to be COMPLETED')

        else:
            self._home_team_score = None
            self._away_team_score = None
            self._winning_team_ID = None
            self._winning_team_score = None
            self._losing_team_ID = None
            self._losing_team_score = None
        
        if not isinstance(status, GameStatus):
            raise TypeError('status must be of type GameStatus')
        self._status = status
        
        if not isinstance(notes, str):
            raise TypeError('notes must be of type str')
        self._notes = notes
        
    @property
    def ID(self):
        return self._ID
        
    @property
    def season_ID(self):
        return self._season_ID
        
    @property
    def week(self):
        return self._week
        
    @property
    def date(self):
        return self._date
        
    @property
    def season_section(self):
        return self._season_section
    
    @property
    def home_team_ID(self):
        return self._home_team_ID
        
    @property
    def away_team_ID(self):
        return self._away_team_ID
        
    @property
    def home_team_score(self):
        return self._home_team_score
        
    @property
    def away_team_score(self):
        return self._away_team_score
        
    @property
    def status(self):
        return self._status
    
    @property
    def notes(self):
        return self._notes
        
    def reschedule(self, week, date_):
        if self.status != GameStatus.SCHEDULED:
            raise GameStatusError('Game can only be rescheduled if it is still scheduled', self.ID, self.status)
        
        if not isinstance(week, int):
            raise TypeError('week must be of type int')
        self._week = week
            
        if not isinstance(date_, date):
            raise TypeError('date_ must be of type date')
        self._date = date_
        
        old_week = self.week
        old_date = self.date
        
        self._event_bus.raise_event(GameRescheduledEvent(self.ID, old_week, old_date, week, date_))
        
    def cancel(self):
        if self.status != GameStatus.SCHEDULED:
            raise GameStatusError('Game can only be canceled if it is still scheduled', self.ID, self.status)
        
        self._status = GameStatus.CANCELED
        self._event_bus.raise_event(GameCanceledEvent(self.ID))
        
    def complete(self, home_team_score, away_team_score):
        if self.status != GameStatus.SCHEDULED:
            raise GameStatusError('Game can only be completed if it is still scheduled', self.ID, self.status)
            
        if home_team_score is None:
            raise ValueError('Home team score cannot be None')

        if away_team_score is None:
            raise ValueError('Away team score cannot be None')
        
        self._set_score(home_team_score, away_team_score)
        self._status = GameStatus.COMPLETED
        
        self._event_bus.raise_event(GameCompletedEvent(self.ID, home_team_score, away_team_score))
        
    def _set_score(self, home_team_score, away_team_score):
        if not isinstance(home_team_score, int):
            raise TypeError('home_team_score must be of type int')
        self._home_team_score = home_team_score
            
        if not isinstance(away_team_score, int):
            raise TypeError('away_team_score must be of type int')
        self._away_team_score = away_team_score
            
        if home_team_score > away_team_score:
            self._winning_team_ID = self.home_team_ID
            self._winning_team_score = self.home_team_score
            self._losing_team_ID = self.away_team_ID
            self._losing_team_score = self.away_team_score
        elif away_team_score > home_team_score:
            self._winning_team_ID = self.away_team_ID
            self._winning_team_score = self.away_team_score
            self._losing_team_ID = self.home_team_ID
            self._losing_team_score = self.home_team_score
        else:
            self._winning_team_ID = None
            self._winning_team_score = None
            self._losing_team_ID = None
            self._losing_team_score = None
            

class GameFactory (object):
    def __init__(self, event_bus):
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._event_bus = event_bus
        
        self._event_bus.register_type(GameScheduledEvent)
        self._event_bus.register_type(GameRescheduledEvent)
        self._event_bus.register_type(GameCanceledEvent)
        self._event_bus.register_type(GameCompletedEvent)
        
    def schedule(self, season, week, date_, season_section, home_team, away_team, notes):
        ID = GameID(uuid4())
        game = Game(self._event_bus, ID, season, week, date_, season_section, home_team, away_team, None, None, GameStatus.SCHEDULED, notes)
        game._event_bus.raise_event(GameScheduledEvent(game.ID, game.season_ID, game.week, game.date, game.season_section, game.home_team_ID, game.away_team_ID, game.notes))
        
        return game


class GameRepository (object):
    def add(self, game):
        raise NotImplementedError

    def find_by_ID(self, ID):
        raise NotImplementedError
        
    def find_season_teams(self, season, season_section, team1, team2):
        raise NotImplementedError
        
    def find_by_season(self, season):
        raise NotImplementedError
        
    def all(self):
        raise NotImplementedError


class GameScheduledEvent (Event):
    def __init__(self, ID, season_ID, week, date_, season_section, home_team_ID, away_team_ID, notes):
        self.ID = ID
        self.season_ID = season_ID
        self.week = week
        self.date = date_
        self.season_section = season_section
        self.home_team_ID = home_team_ID
        self.away_team_ID = away_team_ID
        self.notes = notes
    

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
