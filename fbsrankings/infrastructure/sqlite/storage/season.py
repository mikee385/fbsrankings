import sqlite3

from fbsrankings.domain import SeasonSection


class SeasonSectionTable (object):
    def __init__(self):
        self.name = 'seasonsection'
        self.columns = 'Name'

    def create(self, cursor):
        if not isinstance(cursor, sqlite3.Cursor):
            raise TypeError('cursor must be of type sqlite3.Cursor')
            
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.name}
        (Name TEXT NOT NULL UNIQUE);''')
        
        cursor.execute(f'SELECT {self.columns} from {self.name}')
        existing = [row[0] for row in cursor.fetchall()]
        for value in SeasonSection:
            if value.name not in existing:
                cursor.execute(f'INSERT INTO {self.name} ({self.columns}) VALUES (?)', [value.name])
                    
    def dump(self, connection):
        if not isinstance(connection, sqlite3.Connection):
            raise TypeError('connection must be of type sqlite3.Connection')
            
        print('Season Sections:')
        cursor = connection.cursor()
        cursor.execute(f'SELECT rowid, * FROM {self.name}')
        for row in cursor.fetchall():
            print('(' + ', '.join(str(item) for item in row) + ')')
        cursor.close()
            

class SeasonTable (object):
    def __init__(self):
        self.name = 'season'
        self.columns = 'UUID, Year'
             
    def create(self, cursor):
        if not isinstance(cursor, sqlite3.Cursor):
            raise TypeError('cursor must be of type sqlite3.Cursor')
            
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.name}
            (UUID TEXT NOT NULL UNIQUE,
             Year INT  NOT NULL UNIQUE);''')
                    
    def dump(self, connection):
        if not isinstance(connection, sqlite3.Connection):
            raise TypeError('connection must be of type sqlite3.Connection')

        print('Seasons:')
        cursor = connection.cursor()
        cursor.execute(f'SELECT rowid, * FROM {self.name}')
        for row in cursor.fetchall():
            print('(' + ', '.join(str(item) for item in row) + ')')
        cursor.close()
