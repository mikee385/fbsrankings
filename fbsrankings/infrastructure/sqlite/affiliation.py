import sqlite3
from uuid import UUID

from fbsrankings.common import EventBus
from fbsrankings.domain import Season, SeasonID, Team, TeamID, Affiliation, AffiliationID, AffiliationRepository, Subdivision
from fbsrankings.event import AffiliationRegisteredEvent


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


class AffiliationQueryHandler (AffiliationRepository):
    def __init__(self, connection, event_bus):
        if not isinstance(connection, sqlite3.Connection):
            raise TypeError('connection must be of type sqlite3.Connection')
        self._connection = connection
        
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._event_bus = event_bus
        
        self.table = AffiliationTable()

    def find_by_ID(self, ID):
        if not isinstance(ID, AffiliationID):
            raise TypeError('ID must be of type AffiliationID')
        
        cursor = self._connection.cursor()
        cursor.execute(f'SELECT {self.table.columns} FROM {self.table.name} WHERE UUID=?', [str(ID.value)])
        row = cursor.fetchone()
        cursor.close()
        return self._affiliation_from_row(row)
        
    def find_by_season_team(self, season, team):
        if isinstance(season, Season):
            season_ID = season.ID
        elif isinstance(season, SeasonID):
            season_ID = season
        else:
            raise TypeError('season must be of type Season or SeasonID')
            
        if isinstance(team, Team):
            team_ID = team.ID
        elif isinstance(team, TeamID):
            team_ID = team
        else:
            raise TypeError('team must be of type Team or TeamID')
            
        cursor = self._connection.cursor()
        cursor.execute(f'SELECT {self.table.columns} FROM {self.table.name}  WHERE SeasonID=? AND TeamID=?', [str(season_ID.value), str(team_ID.value)])
        row = cursor.fetchone()
        cursor.close()
        return self._affiliation_from_row(row)
        
    def find_by_season(self, season):
        if isinstance(season, Season):
            season_ID = season.ID
        elif isinstance(season, SeasonID):
            season_ID = season
        else:
            raise TypeError('season must be of type Season or SeasonID')
            
        cursor = self._connection.cursor()
        cursor.execute(f'SELECT {self.table.columns} FROM {self.table.name}  WHERE SeasonID=?', [str(season_ID.value)])
        items = [self._affiliation_from_row(row) for row in cursor.fetchall()]
        cursor.close()
        return items
    
    def _affiliation_from_row(self, row):
        if row is not None:
            return Affiliation(self._event_bus, AffiliationID(UUID(row[0])), SeasonID(UUID(row[1])), TeamID(UUID(row[2])), Subdivision[row[3]])
        else:
            return None
            

class AffiliationEventHandler (object):
    def __init__(self, cursor, event_bus):
        if not isinstance(cursor, sqlite3.Cursor):
            raise TypeError('cursor must be of type sqlite3.Cursor')
        self._cursor = cursor
        
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        event_bus.register_handler(AffiliationRegisteredEvent, self._handle_affiliation_registered)
        
        self.table = AffiliationTable()
        
    def _handle_affiliation_registered(self, event):
        self._cursor.execute(f'INSERT INTO {self.table.name} ({self.table.columns}) VALUES (?, ?, ?, ?)', [str(event.ID.value), str(event.season_ID.value), str(event.team_ID.value), event.subdivision.name])
