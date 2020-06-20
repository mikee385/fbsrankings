import datetime 

from enum import Enum
from typing import Optional, Union
from uuid import UUID, uuid4

from fbsrankings.common import Identifier, EventBus
from fbsrankings.domain import Season, SeasonID, SeasonSection, Team, TeamID
from fbsrankings.event import GameCreatedEvent, GameRescheduledEvent, GameCanceledEvent, GameCompletedEvent, GameNotesUpdatedEvent


class GameStatus (Enum):
    SCHEDULED = 0
    COMPLETED = 1
    CANCELED = 2


class GameID (Identifier):
    pass
    

class GameStatusError (Exception):
    def __init__(self, message: str, game_ID: UUID, status: str) -> None:
        super().__init__(message)
        self.game_ID = game_ID
        self.status = status


class Game (object):
    def __init__(self, bus: EventBus, ID: GameID, season: Union[Season, SeasonID], week: int, date: datetime.date, season_section: SeasonSection, home_team: Union[Team, TeamID], away_team: Union[Team, TeamID], home_team_score: Optional[int], away_team_score: Optional[int], status: GameStatus, notes: str) -> None:
        self._bus = bus
        self._ID = ID
        
        if isinstance(season, Season):
            self._season_ID = season.ID
        elif isinstance(season, SeasonID):
            self._season_ID = season
        else:
            raise TypeError('season must be of type Season or SeasonID')
            
        self._week = week
        self._date = date
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

        self._home_team_score: Optional[int]
        self._away_team_score: Optional[int]
        self._winning_team_ID: Optional[TeamID]
        self._winning_team_score: Optional[int]
        self._losing_team_ID: Optional[TeamID]
        self._losing_team_score: Optional[int]
            
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
        
        self._status = status
        self._notes = notes
        
    @property
    def ID(self) -> GameID:
        return self._ID
        
    @property
    def season_ID(self) -> SeasonID:
        return self._season_ID
        
    @property
    def week(self) -> int:
        return self._week
        
    @property
    def date(self) -> datetime.date:
        return self._date
        
    @property
    def season_section(self) -> SeasonSection:
        return self._season_section
    
    @property
    def home_team_ID(self) -> TeamID:
        return self._home_team_ID
        
    @property
    def away_team_ID(self) -> TeamID:
        return self._away_team_ID
        
    @property
    def home_team_score(self) -> Optional[int]:
        return self._home_team_score
        
    @property
    def away_team_score(self) -> Optional[int]:
        return self._away_team_score
        
    @property
    def winning_team_ID(self) -> Optional[TeamID]:
        return self._winning_team_ID
        
    @property
    def winning_team_score(self) -> Optional[int]:
        return self._winning_team_score
        
    @property
    def losing_team_ID(self) -> Optional[TeamID]:
        return self._losing_team_ID
        
    @property
    def losing_team_score(self) -> Optional[int]:
        return self._losing_team_score
        
    @property
    def status(self) -> GameStatus:
        return self._status
    
    @property
    def notes(self) -> str:
        return self._notes
        
    def reschedule(self, week: int, date: datetime.date) -> None:
        if self.status != GameStatus.SCHEDULED:
            raise GameStatusError('Game can only be rescheduled if it is still scheduled', self.ID.value, self.status.name)
        
        old_week = self._week
        self._week = week
            
        old_date = self._date
        self._date = date

        self._bus.publish(GameRescheduledEvent(self.ID.value, old_week, old_date, week, date))
        
    def cancel(self) -> None:
        if self.status != GameStatus.SCHEDULED:
            raise GameStatusError('Game can only be canceled if it is still scheduled', self.ID.value, self.status.name)
        
        self._status = GameStatus.CANCELED
        
        self._bus.publish(GameCanceledEvent(self.ID.value))
        
    def complete(self, home_team_score: int, away_team_score: int) -> None:
        if self.status != GameStatus.SCHEDULED:
            raise GameStatusError('Game can only be completed if it is still scheduled', self.ID.value, self.status.name)
            
        if home_team_score is None:
            raise ValueError('Home team score cannot be None')

        if away_team_score is None:
            raise ValueError('Away team score cannot be None')
        
        self._set_score(home_team_score, away_team_score)

        self._status = GameStatus.COMPLETED
        
        self._bus.publish(GameCompletedEvent(self.ID.value, home_team_score, away_team_score))
        
    def _set_score(self, home_team_score: int, away_team_score: int) -> None:
        self._home_team_score = home_team_score
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

    def update_notes(self, notes: str) -> None:
        old_notes = self._notes
        self._notes = notes
        
        self._bus.publish(GameNotesUpdatedEvent(self.ID.value, old_notes, notes))


class GameRepository (object):
    def __init__(self, bus: EventBus) -> None:
        self._bus = bus
        
    def create(self, season: Union[Season, SeasonID], week: int, date: datetime.date, season_section: SeasonSection, home_team: Union[Team, TeamID], away_team: Union[Team, TeamID], notes: str) -> Game:
        ID = GameID(uuid4())
        game = Game(self._bus, ID, season, week, date, season_section, home_team, away_team, None, None, GameStatus.SCHEDULED, notes)
        self._bus.publish(GameCreatedEvent(game.ID.value, game.season_ID.value, game.week, game.date, game.season_section.name, game.home_team_ID.value, game.away_team_ID.value, game.notes))
        
        return game
    
    def get(self, ID: GameID) -> Optional[Game]:
        raise NotImplementedError
        
    def find(self, season: Union[Season, SeasonID], week: int, team1: Union[Team, TeamID], team2: Union[Team, TeamID]) -> Optional[Game]:
        raise NotImplementedError
