import sqlite3


class TeamTable (object):
    def __init__(self) -> None:
        self.name = 'team'
        self.columns = 'UUID, Name'
        
    def create(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.name}
            (UUID TEXT NOT NULL UNIQUE,
             Name TEXT NOT NULL UNIQUE);''')
             
    def dump(self, connection: sqlite3.Connection) -> None:
        print('Teams:')
        cursor = connection.cursor()
        cursor.execute(f'SELECT rowid, * FROM {self.name}')
        for row in cursor.fetchall():
            print('(' + ', '.join(str(item) for item in row) + ')')
        cursor.close()
