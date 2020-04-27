import sqlite3
from datetime import datetime
from uuid import UUID

from fbsrankings.common import EventBus
from fbsrankings.domain import Season, SeasonID, SeasonSection, Team, TeamID, Game, GameID, GameStatus, GameRepository as BaseRepository, GameScheduledEvent, GameRescheduledEvent, GameCanceledEvent, GameCompletedEvent


class GameStatusTable (object):
    def __init__(self, connection):
        if not isinstance(connection, sqlite3.Connection):
            raise TypeError('connection must be of type sqlite3.Connection')
        self._connection = connection
        
        self._table = 'gamestatus'
        self._columns = 'Name'
        
        with self._connection:
            self._connection.execute('BEGIN')
            cursor = self._connection.cursor()
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self._table}
            (Name TEXT NOT NULL UNIQUE);''')
            cursor.execute(f'SELECT {self._columns} from {self._table}')
            existing = [row[0] for row in cursor.fetchall()]
            for value in GameStatus:
                if value.name not in existing:
                    cursor.execute(f'INSERT INTO {self._table} ({self._columns}) VALUES (?)', [value.name])
                    
    def dump(self):
        print('Game Statuses:')
        cursor = self._connection.cursor()
        cursor.execute(f'SELECT rowid, * FROM {self._table}')
        for row in cursor.fetchall():
            print('(' + ', '.join(str(item) for item in row) + ')')
            

class GameRepository (BaseRepository):
    def __init__(self, connection, event_bus):
        if not isinstance(connection, sqlite3.Connection):
            raise TypeError('connection must be of type sqlite3.Connection')
        self._connection = connection
        
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._event_bus = event_bus
        
        self.game_status = GameStatusTable(self._connection)
        
        self._table = 'game'
        self._columns = 'UUID, SeasonID, Week, Date, SeasonSection, HomeTeamID, AwayTeamID, HomeTeamScore, AwayTeamScore, Status, Notes'
        
        cursor = self._connection.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self._table}
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

    def find_by_ID(self, ID):
        if not isinstance(ID, GameID):
            raise TypeError('ID must be of type GameID')
        
        cursor = self._connection.cursor()
        cursor.execute(f'SELECT {self._columns} FROM {self._table} WHERE UUID=?', [str(ID.value)])
        row = cursor.fetchone()
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
        cursor.execute(f'SELECT {self._columns} FROM {self._table}  WHERE SeasonID=? AND Week=? AND ((HomeTeamID=? AND AwayTeamID=?) OR (AwayTeamID=? AND HomeTeamID=?))', [str(season_ID.value), week, str(team1_ID.value), str(team2_ID.value), str(team1_ID.value), str(team2_ID.value)])
        row = cursor.fetchone()
        return self._game_from_row(row)
        
    def find_by_season(self, season):
        if isinstance(season, Season):
            season_ID = season.ID
        elif isinstance(season, SeasonID):
            season_ID = season
        else:
            raise TypeError('season must be of type Season or SeasonID')
            
        cursor = self._connection.cursor()
        cursor.execute(f'SELECT {self._columns} FROM {self._table}  WHERE SeasonID=?', [str(season_ID.value)])
        return [self._game_from_row(row) for row in cursor.fetchall()]
        
    def all(self):
        cursor = self._connection.cursor()
        cursor.execute(f'SELECT {self._columns} FROM {self._table}')
        return [self._game_from_row(row) for row in cursor.fetchall()]
        
    def dump(self):
        print('Games:')
        cursor = self._connection.cursor()
        cursor.execute(f'SELECT rowid, * FROM {self._table}')
        for row in cursor.fetchall():
            print('(' + ', '.join(str(item) for item in row) + ')')
            
    def _game_from_row(self, row):
        if row is not None:
            return Game(self._event_bus, GameID(UUID(row[0])), SeasonID(UUID(row[1])), row[2], datetime.strptime(row[3], '%Y-%m-%d').date(), SeasonSection[row[4]], TeamID(UUID(row[5])), TeamID(UUID(row[6])), row[7], row[8], GameStatus[row[9]], row[10])
        else:
            return None
        
    def try_handle_event(self, event):
        if isinstance(event, GameScheduledEvent):
            cursor = self._connection.cursor()
            cursor.execute(f'INSERT INTO {self._table} ({self._columns}) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', [str(event.ID.value), str(event.season_ID.value), event.week, event.date, event.season_section.name, str(event.home_team_ID.value), str(event.away_team_ID.value), None, None, GameStatus.SCHEDULED.name, event.notes])
            return True
        elif isinstance(event, GameRescheduledEvent):
            cursor = self._connection.cursor()
            cursor.execute(f'UPDATE {self._table} SET Week=?, Date=? WHERE UUID=?', [event.week, event.date, str(event.ID.value)])
            return True
        elif isinstance(event, GameCanceledEvent):
            cursor = self._connection.cursor()
            cursor.execute(f'UPDATE {self._table} SET Status=? WHERE UUID=?', [GameStatus.CANCELED.name, str(event.ID.value)])
            return True
        elif isinstance(event, GameCompletedEvent):
            cursor = self._connection.cursor()
            cursor.execute(f'UPDATE {self._table} SET HomeTeamScore=?, AwayTeamScore=?, Status=? WHERE UUID=?', [event.home_team_score, event.away_team_score, GameStatus.COMPLETED.name, str(event.ID.value)])
            return True
        else:
            return False
