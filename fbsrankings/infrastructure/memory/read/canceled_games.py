from fbsrankings.query import CanceledGamesResult, CanceledGameResult
from fbsrankings.domain import GameStatus
from fbsrankings.infrastructure.memory.storage import Storage


class CanceledGamesQueryHandler (object):
    def __init__(self, storage):
        if not isinstance(storage, Storage):
            raise TypeError('storage must be of type Storage')
        self._storage = storage

    def handle(self, query):
        games = []
        for game in self._storage.game.all():
            if game.status == GameStatus.CANCELED:
                season = self._storage.season.get(game.season_ID)
                home_team = self._storage.team.get(game.home_team_ID)
                away_team = self._storage.team.get(game.away_team_ID)
                games.append(CanceledGameResult(game.ID, game.season_ID, season.year, game.week, game.date, game.season_section, game.home_team_ID, home_team.name, game.away_team_ID, away_team.name, game.notes))
        
        return CanceledGamesResult(games)
