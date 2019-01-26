import sqlite3
from uuid import UUID

from fbsrankings.common import EventBus
from fbsrankings.domain import Season, SeasonID, Team, TeamID, Affiliation, AffiliationID, AffiliationRepository as BaseRepository, Subdivision, AffiliationRegisteredEvent


class SubdivisionTable (object):
    def __init__(self, connection):
        if not isinstance(connection, sqlite3.Connection):
            raise TypeError('connection must be of type sqlite3.Connection')
        self._connection = connection
        
        self._table = 'subdivision'
        self._columns = 'Name'
        
        with self._connection:
            self._connection.execute('BEGIN')
            cursor = self._connection.cursor()
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self._table}
            (Name TEXT NOT NULL UNIQUE);''')
            cursor.execute(f'SELECT {self._columns} from {self._table}')
            existing = [row[0] for row in cursor.fetchall()]
            for value in Subdivision:
                if value.name not in existing:
                    cursor.execute(f'INSERT INTO {self._table} ({self._columns}) VALUES (?)', [value.name])
                    
    def dump(self):
        print('Subdivisions:')
        cursor = self._connection.cursor()
        cursor.execute(f'SELECT rowid, * FROM {self._table}')
        for row in cursor.fetchall():
            print('(' + ', '.join(str(item) for item in row) + ')')


class AffiliationRepository (BaseRepository):
    def __init__(self, connection, event_bus):
        if not isinstance(connection, sqlite3.Connection):
            raise TypeError('connection must be of type sqlite3.Connection')
        self._connection = connection
        
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._event_bus = event_bus
        
        self.subdivision = SubdivisionTable(self._connection)
        
        self._table = 'affiliation'
        self._columns = 'UUID, SeasonID, TeamID, Subdivision'
        
        cursor = self._connection.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self._table}
            (UUID TEXT NOT NULL UNIQUE,
             SeasonID TEXT NOT NULL REFERENCES season(UUID),
             TeamID TEXT NOT NULL REFERENCES team(UUID),
             Subdivision TEXT NOT NULL REFERENCES subdivision(Name), UNIQUE(SeasonID, TeamID));''')
        
    def add(self, affiliation):
        # Handled through events
        pass

    def find_by_ID(self, ID):
        if not isinstance(ID, AffiliationID):
            raise TypeError('ID must be of type AffiliationID')
        
        cursor = self._connection.cursor()
        cursor.execute(f'SELECT {self._columns} FROM {self._table} WHERE UUID=?', [str(ID.value)])
        row = cursor.fetchone()
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
        cursor.execute(f'SELECT {self._columns} FROM {self._table}  WHERE SeasonID=? AND TeamID=?', [str(season_ID.value), str(team_ID.value)])
        row = cursor.fetchone()
        return self._affiliation_from_row(row)
        
    def find_by_season(self, season):
        if isinstance(season, Season):
            season_ID = season.ID
        elif isinstance(season, SeasonID):
            season_ID = season
        else:
            raise TypeError('season must be of type Season or SeasonID')
            
        cursor = self._connection.cursor()
        cursor.execute(f'SELECT {self._columns} FROM {self._table}  WHERE SeasonID=?', [str(season_ID.value)])
        return [self._affiliation_from_row(row) for row in cursor.fetchall()]
        
    def dump(self):
        print('Affiliations:')
        cursor = self._connection.cursor()
        cursor.execute(f'SELECT rowid, * FROM {self._table}')
        for row in cursor.fetchall():
            print('(' + ', '.join(str(item) for item in row) + ')')
    
    def _affiliation_from_row(self, row):
        if row is not None:
            return Affiliation(self._event_bus, AffiliationID(UUID(row[0])), SeasonID(UUID(row[1])), TeamID(UUID(row[2])),
            Subdivision[row[3]])
        else:
            return None
        
    def try_handle_event(self, event):
        if isinstance(event, AffiliationRegisteredEvent):
            cursor = self._connection.cursor()
            cursor.execute(f'INSERT INTO {self._table} ({self._columns}) VALUES (?, ?, ?, ?)', [str(event.ID.value), str(event.season_ID.value), str(event.team_ID.value), event.subdivision.name])
            return True
        else:
            return False
