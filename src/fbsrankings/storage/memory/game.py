import datetime
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple

from dataclasses import dataclass


@dataclass
class GameDto:
    id_: str
    season_id: str
    week: int
    date: datetime.date
    season_section: str
    home_team_id: str
    away_team_id: str
    home_team_score: Optional[int]
    away_team_score: Optional[int]
    status: str
    notes: str


class GameStorage:
    def __init__(self) -> None:
        self._by_id: Dict[str, GameDto] = {}
        self._by_key: Dict[Tuple[str, int, str, str], GameDto] = {}
        self._by_season: Dict[str, List[GameDto]] = {}

    @staticmethod
    def _get_key(
        season_id: str,
        week: int,
        team1_id: str,
        team2_id: str,
    ) -> Tuple[str, int, str, str]:
        if team1_id < team2_id:
            return (season_id, week, team1_id, team2_id)
        return (season_id, week, team2_id, team1_id)

    def add(self, game: GameDto) -> None:
        key = self._get_key(
            game.season_id,
            game.week,
            game.home_team_id,
            game.away_team_id,
        )
        if key in self._by_key:
            raise ValueError(
                f"Game already exists for week {game.week} in season {game.season_id}"
                f" between {game.home_team_id} and {game.away_team_id}",
            )

        self._by_id[game.id_] = game
        self._by_key[key] = game

        by_season = self._by_season.get(game.season_id)
        if by_season is None:
            by_season = []
            self._by_season[game.season_id] = by_season
        by_season.append(game)

    def get(self, id_: str) -> Optional[GameDto]:
        return self._by_id.get(id_)

    def find(
        self,
        season_id: str,
        week: int,
        team1_id: str,
        team2_id: str,
    ) -> Optional[GameDto]:
        key = self._get_key(season_id, week, team1_id, team2_id)
        return self._by_key.get(key)

    def for_season(self, season_id: str) -> List[GameDto]:
        by_season = self._by_season.get(season_id)
        if by_season is None:
            return []
        return list(by_season)

    def all_(self) -> Iterable[GameDto]:
        return self._by_key.values()

    def drop(self) -> None:
        self._by_id = {}
        self._by_key = {}
        self._by_season = {}
