import sqlite3
from datetime import datetime
from uuid import UUID

from fbsrankings.domain import Season, SeasonID, SeasonSection, Team, TeamID, Game, GameID, GameStatus, GameRepository as BaseRepository
from fbsrankings.event import GameScheduledEvent, GameRescheduledEvent, GameCanceledEvent, GameCompletedEvent, GameNotesUpdatedEvent
from fbsrankings.infrastructure.sqlite.storage import GameTable


class GameRepository (BaseRepository):
    def __init__(self, connection, cursor, bus):
        super().__init__(bus)
        
        if not isinstance(connection, sqlite3.Connection):
            raise TypeError('connection must be of type sqlite3.Connection')
        self._connection = connection
        
        if not isinstance(cursor, sqlite3.Cursor):
            raise TypeError('cursor must be of type sqlite3.Cursor')
        self._cursor = cursor
        
        self.table = GameTable()
        
        bus.register_handler(GameScheduledEvent, self._handle_game_scheduled)
        bus.register_handler(GameRescheduledEvent, self._handle_game_rescheduled)
        bus.register_handler(GameCanceledEvent, self._handle_game_canceled)
        bus.register_handler(GameCompletedEvent, self._handle_game_completed)
        bus.register_handler(GameNotesUpdatedEvent, self._handle_game_notes_updated)

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
            return Game(self._bus, GameID(UUID(row[0])), SeasonID(UUID(row[1])), row[2], datetime.strptime(row[3], '%Y-%m-%d').date(), SeasonSection[row[4]], TeamID(UUID(row[5])), TeamID(UUID(row[6])), row[7], row[8], GameStatus[row[9]], row[10])
        else:
            return None

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