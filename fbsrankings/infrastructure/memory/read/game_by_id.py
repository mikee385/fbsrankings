from typing import Optional

from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.query import GameByIDQuery
from fbsrankings.query import GameByIDResult


class GameByIDQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: GameByIDQuery) -> Optional[GameByIDResult]:
        game = self._storage.game.get(query.id)
        if game is not None:
            season = self._storage.season.get(game.season_id)
            home_team = self._storage.team.get(game.home_team_id)
            away_team = self._storage.team.get(game.away_team_id)

            if season is not None and home_team is not None and away_team is not None:
                return GameByIDResult(
                    game.id,
                    game.season_id,
                    season.year,
                    game.week,
                    game.date,
                    game.season_section,
                    game.home_team_id,
                    home_team.name,
                    game.away_team_id,
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
