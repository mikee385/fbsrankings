import sqlite3
from uuid import UUID

from fbsrankings.query import GameByIDResult
from fbsrankings.domain import SeasonSection, GameStatus
from fbsrankings.infrastructure.sqlite.storage import SeasonTable, TeamTable, GameTable


class GameByIDQueryHandler (object):
    def __init__(self, connection):
        if not isinstance(connection, sqlite3.Connection):
            raise TypeError('connection must be of type sqlite3.Connection')
        self._connection = connection
        
        self.season_table = SeasonTable()
        self.team_table = TeamTable()
        self.game_table = GameTable()

    def handle(self, query):
        cursor = self._connection.cursor()
        cursor.execute(f'SELECT game.UUID, game.SeasonID, season.Year, game.Week, game.Date, game.SeasonSection, game.HomeTeamID, home_team.Name, game.AwayTeamID, away_team.name, game.HomeTeamScore, game.AwayTeamScore, game.Status, game.Notes FROM {self.game_table.name} AS game INNER JOIN {self.season_table.name} AS season ON season.UUID = game.SeasonID INNER JOIN {self.team_table.name} AS home_team ON home_team.UUID = game.HomeTeamID INNER JOIN {self.team_table.name} AS away_team ON away_team.UUID = game.AwayTeamID WHERE game.UUID=?', [str(query.ID)])
        row = cursor.fetchone()
        cursor.close()
        
        if row:
            return GameByIDResult(UUID(row[0]), UUID(row[1]), row[2], row[3], row[4], SeasonSection[row[5]], UUID(row[6]), row[7], UUID(row[8]), row[9], row[10], row[11], GameStatus[row[12]], row[13])
        else:
            return None