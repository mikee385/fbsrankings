import sqlite3

from fbsrankings.domain import Subdivision


class SubdivisionTable (object):
    def __init__(self):
        self.name = 'subdivision'
        self.columns = 'Name'
        
    def create(self, cursor):
        if not isinstance(cursor, sqlite3.Cursor):
            raise TypeError('cursor must be of type sqlite3.Cursor')
        
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.name}
        (Name TEXT NOT NULL UNIQUE);''')
        
        cursor.execute(f'SELECT {self.columns} from {self.name}')
        existing = [row[0] for row in cursor.fetchall()]
        for value in Subdivision:
            if value.name not in existing:
                cursor.execute(f'INSERT INTO {self.name} ({self.columns}) VALUES (?)', [value.name])
                    
    def dump(self, connection):
        if not isinstance(connection, sqlite3.Connection):
            raise TypeError('connection must be of type sqlite3.Connection')

        print('Subdivisions:')
        cursor = connection.cursor()
        cursor.execute(f'SELECT rowid, * FROM {self.name}')
        for row in cursor.fetchall():
            print('(' + ', '.join(str(item) for item in row) + ')')
        cursor.close()
            
            
class AffiliationTable (object):
    def __init__(self):
        self.name = 'affiliation'
        self.columns = 'UUID, SeasonID, TeamID, Subdivision'
        
    def create(self, cursor):
        if not isinstance(cursor, sqlite3.Cursor):
            raise TypeError('cursor must be of type sqlite3.Cursor')
            
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.name}
            (UUID TEXT NOT NULL UNIQUE,
             SeasonID TEXT NOT NULL REFERENCES season(UUID),
             TeamID TEXT NOT NULL REFERENCES team(UUID),
             Subdivision TEXT NOT NULL REFERENCES subdivision(Name), UNIQUE(SeasonID, TeamID));''')
             
    def dump(self, connection):
        if not isinstance(connection, sqlite3.Connection):
            raise TypeError('connection must be of type sqlite3.Connection')

        print('Affiliations:')
        cursor = connection.cursor()
        cursor.execute(f'SELECT rowid, * FROM {self.name}')
        for row in cursor.fetchall():
            print('(' + ', '.join(str(item) for item in row) + ')')
        cursor.close()
