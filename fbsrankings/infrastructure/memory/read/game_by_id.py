from typing import Optional

from fbsrankings.common import QueryHandler
from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.query import GameByIDQuery, GameByIDResult


class GameByIDQueryHandler(QueryHandler[GameByIDQuery, Optional[GameByIDResult]]):
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def handle(self, query: GameByIDQuery) -> Optional[GameByIDResult]:
        game = self._storage.game.get(query.ID)
        if game is not None:
            season = self._storage.season.get(game.season_ID)
            home_team = self._storage.team.get(game.home_team_ID)
            away_team = self._storage.team.get(game.away_team_ID)

            if season is not None and home_team is not None and away_team is not None:
                return GameByIDResult(
                    game.ID,
                    game.season_ID,
                    season.year,
                    game.week,
                    game.date,
                    game.season_section,
                    game.home_team_ID,
                    home_team.name,
                    game.away_team_ID,
                    away_team.name,
                    game.home_team_score,
                    game.away_team_score,
                    game.status,
                    game.notes,
                )
            else:
                return None
        else:
            return None
