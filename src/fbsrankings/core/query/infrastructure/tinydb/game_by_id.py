from datetime import datetime
from typing import Optional

from fbsrankings.messages.query import GameByIDQuery
from fbsrankings.messages.query import GameByIDResult
from fbsrankings.storage.tinydb import Storage


class GameByIDQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: GameByIDQuery) -> Optional[GameByIDResult]:
        item = self._storage.cache_game_by_id.get(query.game_id)

        return (
            GameByIDResult(
                item["id_"],
                item["season_id"],
                item["year"],
                item["week"],
                datetime.strptime(item["date"], "%Y-%m-%d").date(),
                item["season_section"],
                item["home_team_id"],
                item["home_team_name"],
                item["away_team_id"],
                item["away_team_name"],
                item["home_team_score"],
                item["away_team_score"],
                item["status"],
                item["notes"],
            )
            if item is not None
            else None
        )
