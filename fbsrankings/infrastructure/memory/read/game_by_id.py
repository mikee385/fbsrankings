from fbsrankings.query import GameByIDResult
from fbsrankings.infrastructure.memory.storage import Storage


class GameByIDQueryHandler (object):
    def __init__(self, storage):
        if not isinstance(storage, Storage):
            raise TypeError('storage must be of type Storage')
        self._storage = storage

    def handle(self, query):
        game = self._storage.game.get(query.ID)
        if game is not None:
            season = self._storage.season.get(game.season_ID)
            home_team = self._storage.team.get(game.home_team_ID)
            away_team = self._storage.team.get(game.away_team_ID)
                
            return GameByIDResult(game.ID, game.season_ID, season.year, game.week, game.date, game.season_section, game.home_team_ID, home_team.name, game.away_team_ID, away_team.name, game.home_team_score, game.away_team_score, game.status, game.notes)
        else:
            return None
