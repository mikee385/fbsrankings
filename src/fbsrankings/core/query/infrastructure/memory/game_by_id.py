from typing import Optional

from fbsrankings.messages.convert import date_to_timestamp
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
                    game_id=str(game.id_),
                    season_id=str(game.season_id),
                    year=season.year,
                    week=game.week,
                    date=date_to_timestamp(game.date),
                    season_section=game.season_section,
                    home_team_id=str(game.home_team_id),
                    home_team_name=home_team.name,
                    away_team_id=str(game.away_team_id),
                    away_team_name=away_team.name,
                    home_team_score=game.home_team_score,
                    away_team_score=game.away_team_score,
                    status=game.status,
                    notes=game.notes,
                )
        return None
