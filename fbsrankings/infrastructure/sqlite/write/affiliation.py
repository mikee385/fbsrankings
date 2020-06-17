import sqlite3
from uuid import UUID

from fbsrankings.domain import Season, SeasonID, Team, TeamID, Affiliation, AffiliationID, AffiliationRepository as BaseRepository, Subdivision
from fbsrankings.event import AffiliationRegisteredEvent
from fbsrankings.infrastructure.sqlite.storage import AffiliationTable


class AffiliationRepository (BaseRepository):
    def __init__(self, connection, cursor, bus):
        super().__init__(bus)
        
        if not isinstance(connection, sqlite3.Connection):
            raise TypeError('connection must be of type sqlite3.Connection')
        self._connection = connection
        
        if not isinstance(cursor, sqlite3.Cursor):
            raise TypeError('cursor must be of type sqlite3.Cursor')
        self._cursor = cursor
        
        self.table = AffiliationTable()
    
        bus.register_handler(AffiliationRegisteredEvent, self._handle_affiliation_registered)

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
            return Affiliation(self._bus, AffiliationID(UUID(row[0])), SeasonID(UUID(row[1])), TeamID(UUID(row[2])), Subdivision[row[3]])
        else:
            return None
        
    def _handle_affiliation_registered(self, event):
        self._cursor.execute(f'INSERT INTO {self.table.name} ({self.table.columns}) VALUES (?, ?, ?, ?)', [str(event.ID.value), str(event.season_ID.value), str(event.team_ID.value), event.subdivision.name])
