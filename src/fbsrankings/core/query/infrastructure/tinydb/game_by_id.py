from datetime import datetime
from typing import Optional

from fbsrankings.messages.convert import datetime_to_timestamp
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
                game_id=item["id_"],
                season_id=item["season_id"],
                year=item["year"],
                week=item["week"],
                date=datetime_to_timestamp(datetime.strptime(item["date"], "%Y-%m-%d")),
                season_section=item["season_section"],
                home_team_id=item["home_team_id"],
                home_team_name=item["home_team_name"],
                away_team_id=item["away_team_id"],
                away_team_name=item["away_team_name"],
                home_team_score=item["home_team_score"],
                away_team_score=item["away_team_score"],
                status=item["status"],
                notes=item["notes"],
            )
            if item is not None
            else None
        )
