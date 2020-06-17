import sqlite3

from fbsrankings.domain import GameStatus


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
