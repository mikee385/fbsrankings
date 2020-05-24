import sqlite3
from datetime import datetime
from uuid import UUID

from fbsrankings.common import EventBus
from fbsrankings.domain import Season, SeasonID, SeasonSection, Team, TeamID, Game, GameID, GameStatus, GameRepository
from fbsrankings.event import GameScheduledEvent, GameRescheduledEvent, GameCanceledEvent, GameCompletedEvent, GameNotesUpdatedEvent


class GameStatusTable (object):
    def __init__(self):
        self.name = 'gamestatus'
        self.columns = 'Name'
        
    def create(self, cursor):
        if not isinstance(cursor, sqlite3.Cursor):
            raise TypeError('cursor must be of type sqlite3.Cursor')
        
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.name}
        (Name TEXT NOT NULL UNIQUE);''')
        
        cursor.execute(f'SELECT {self.columns} from {self.name}')
        existing = [row[0] for row in cursor.fetchall()]
        for value in GameStatus:
            if value.name not in existing:
                cursor.execute(f'INSERT INTO {self.name} ({self.columns}) VALUES (?)', [value.name])
                    
    def dump(self, connection):
        if not isinstance(connection, sqlite3.Connection):
            raise TypeError('connection must be of type sqlite3.Connection')
            
        print('Game Statuses:')
        cursor = connection.cursor()
        cursor.execute(f'SELECT rowid, * FROM {self.name}')
        for row in cursor.fetchall():
            print('(' + ', '.join(str(item) for item in row) + ')')
        cursor.close()
        
        
class GameTable (object):
    def __init__(self):
        self.name = 'game'
        self.columns = 'UUID, SeasonID, Week, Date, SeasonSection, HomeTeamID, AwayTeamID, HomeTeamScore, AwayTeamScore, Status, Notes'
        
    def create(self, cursor):
        if not isinstance(cursor, sqlite3.Cursor):
            raise TypeError('cursor must be of type sqlite3.Cursor')
            
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.name}
            (UUID TEXT NOT NULL UNIQUE,
             SeasonID TEXT NOT NULL REFERENCES season(UUID),
             Week INT NOT NULL,
             Date DATE NOT NULL,
             SeasonSection TEXT NOT NULL REFERENCES seasonsection(Name),
             HomeTeamID TEXT NOT NULL REFERENCES team(UUID),
             AwayTeamID TEXT NOT NULL REFERENCES team(UUID),
             HomeTeamScore INT NULL,
             AwayTeamScore INT NULL,
             Status TEXT NOT NULL REFERENCES gamestatus(Name),
             Notes TEXT NOT NULL, UNIQUE(SeasonID, Week, HomeTeamID, AwayTeamID));''')
             
    def dump(self, connection):
        if not isinstance(connection, sqlite3.Connection):
            raise TypeError('connection must be of type sqlite3.Connection')
        
        print('Games:')
        cursor = connection.cursor()
        cursor.execute(f'SELECT rowid, * FROM {self.name}')
        for row in cursor.fetchall():
            print('(' + ', '.join(str(item) for item in row) + ')')
        cursor.close()


class GameQueryHandler (GameRepository):
    def __init__(self, connection, event_bus):
        if not isinstance(connection, sqlite3.Connection):
            raise TypeError('connection must be of type sqlite3.Connection')
        self._connection = connection
        
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._event_bus = event_bus
        
        self.table = GameTable()

    def find_by_ID(self, ID):
        if not isinstance(ID, GameID):
            raise TypeError('ID must be of type GameID')
        
        cursor = self._connection.cursor()
        cursor.execute(f'SELECT {self.table.columns} FROM {self.table.name} WHERE UUID=?', [str(ID.value)])
        row = cursor.fetchone()
        cursor.close()
        return self._game_from_row(row)
        
    def find_by_season_teams(self, season, week, team1, team2):
        if isinstance(season, Season):
            season_ID = season.ID
        elif isinstance(season, SeasonID):
            season_ID = season
        else:
            raise TypeError('season must be of type Season or SeasonID')
            
        if isinstance(team1, Team):
            team1_ID = team1.ID
        elif isinstance(team1, TeamID):
            team1_ID = team1
        else:
            raise TypeError('team1 must be of type Team or TeamID')
            
        if isinstance(team2, Team):
            team2_ID = team2.ID
        elif isinstance(team2, TeamID):
            team2_ID = team2
        else:
            raise TypeError('team2 must be of type Team or TeamID')
            
        cursor = self._connection.cursor()
        cursor.execute(f'SELECT {self.table.columns} FROM {self.table.name}  WHERE SeasonID=? AND Week=? AND ((HomeTeamID=? AND AwayTeamID=?) OR (AwayTeamID=? AND HomeTeamID=?))', [str(season_ID.value), week, str(team1_ID.value), str(team2_ID.value), str(team1_ID.value), str(team2_ID.value)])
        row = cursor.fetchone()
        cursor.close()
        return self._game_from_row(row)
        
    def find_by_season(self, season):
        if isinstance(season, Season):
            season_ID = season.ID
        elif isinstance(season, SeasonID):
            season_ID = season
        else:
            raise TypeError('season must be of type Season or SeasonID')
            
        cursor = self._connection.cursor()
        cursor.execute(f'SELECT {self.table.columns} FROM {self.table.name}  WHERE SeasonID=?', [str(season_ID.value)])
        items = [self._game_from_row(row) for row in cursor.fetchall()]
        cursor.close()
        return items
        
    def all(self):
        cursor = self._connection.cursor()
        cursor.execute(f'SELECT {self.table.columns} FROM {self.table.name}')
        items = [self._game_from_row(row) for row in cursor.fetchall()]
        cursor.close()
        return items
            
    def _game_from_row(self, row):
        if row is not None:
            return Game(self._event_bus, GameID(UUID(row[0])), SeasonID(UUID(row[1])), row[2], datetime.strptime(row[3], '%Y-%m-%d').date(), SeasonSection[row[4]], TeamID(UUID(row[5])), TeamID(UUID(row[6])), row[7], row[8], GameStatus[row[9]], row[10])
        else:
            return None
            

class GameEventHandler (object):
    def __init__(self, cursor, event_bus):
        if not isinstance(cursor, sqlite3.Cursor):
            raise TypeError('cursor must be of type sqlite3.Cursor')
        self._cursor = cursor
        
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        event_bus.register_handler(GameScheduledEvent, self._handle_game_scheduled)
        event_bus.register_handler(GameRescheduledEvent, self._handle_game_rescheduled)
        event_bus.register_handler(GameCanceledEvent, self._handle_game_canceled)
        event_bus.register_handler(GameCompletedEvent, self._handle_game_completed)
        event_bus.register_handler(GameNotesUpdatedEvent, self._handle_game_notes_updated)
        
        self.table = GameTable()
        
    def handle(self, event):
        if isinstance(event, GameScheduledEvent):
            self._handle_game_scheduled(event)
            return True
        elif isinstance(event, GameRescheduledEvent):
            self._handle_game_rescheduled(event)
            return True
        elif isinstance(event, GameCanceledEvent):
            self._handle_game_canceled(event)
            return True
        elif isinstance(event, GameCompletedEvent):
            self._handle_game_completed(event)
            return True
        elif isinstance(event, GameNotesUpdatedEvent):
            self._handle_game_notes_updated(event)
            return True
        else:
            return False
        
    def _handle_game_scheduled(self, event):
        self._cursor.execute(f'INSERT INTO {self.table.name} ({self.table.columns}) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', [str(event.ID.value), str(event.season_ID.value), event.week, event.date, event.season_section.name, str(event.home_team_ID.value), str(event.away_team_ID.value), None, None, GameStatus.SCHEDULED.name, event.notes])
    
    def _handle_game_rescheduled(self, event):
        self._cursor.execute(f'UPDATE {self.table.name} SET Week=?, Date=? WHERE UUID=?', [event.week, event.date, str(event.ID.value)])
    
    def _handle_game_canceled(self, event):
        self._cursor.execute(f'UPDATE {self.table.name} SET Status=? WHERE UUID=?', [GameStatus.CANCELED.name, str(event.ID.value)])
    
    def _handle_game_completed(self, event):
        self._cursor.execute(f'UPDATE {self.table.name} SET HomeTeamScore=?, AwayTeamScore=?, Status=? WHERE UUID=?', [event.home_team_score, event.away_team_score, GameStatus.COMPLETED.name, str(event.ID.value)])
    
    def _handle_game_notes_updated(self, event):
        self._cursor.execute(f'UPDATE {self.table.name} SET Notes=? WHERE UUID=?', [event.notes, str(event.ID.value)])
