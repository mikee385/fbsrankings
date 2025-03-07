from typing import Optional

from fbsrankings.messages.query import GameByIDQuery
from fbsrankings.messages.query import GameByIDResult
from fbsrankings.storage.memory import Storage


class GameByIDQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: GameByIDQuery) -> Optional[GameByIDResult]:
        game = self._storage.game.get(query.game_id)
        if game is not None:
            season = self._storage.season.get(game.season_id)
            home_team = self._storage.team.get(game.home_team_id)
            away_team = self._storage.team.get(game.away_team_id)

            if season is not None and home_team is not None and away_team is not None:
                return GameByIDResult(
                    str(game.id_),
                    str(game.season_id),
                    season.year,
                    game.week,
                    game.date,
                    game.season_section,
                    str(game.home_team_id),
                    home_team.name,
                    str(game.away_team_id),
                    away_team.name,
                    game.home_team_score,
                    game.away_team_score,
                    game.status,
                    game.notes,
                )
        return None
