import datetime
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple
from uuid import UUID


class GameDto:
    def __init__(
        self,
        id_: UUID,
        season_id: UUID,
        week: int,
        date: datetime.date,
        season_section: str,
        home_team_id: UUID,
        away_team_id: UUID,
        home_team_score: Optional[int],
        away_team_score: Optional[int],
        status: str,
        notes: str,
    ) -> None:
        self.id_ = id_
        self.season_id = season_id
        self.week = week
        self.date = date
        self.season_section = season_section
        self.home_team_id = home_team_id
        self.away_team_id = away_team_id
        self.home_team_score = home_team_score
        self.away_team_score = away_team_score
        self.status = status
        self.notes = notes


class GameStorage:
    def __init__(self) -> None:
        self._by_id: Dict[UUID, GameDto] = {}
        self._by_key: Dict[Tuple[UUID, int, UUID, UUID], GameDto] = {}
        self._by_season: Dict[UUID, List[GameDto]] = {}

    @staticmethod
    def _get_key(
        season_id: UUID, week: int, team1_id: UUID, team2_id: UUID,
    ) -> Tuple[UUID, int, UUID, UUID]:
        if team1_id < team2_id:
            return (season_id, week, team1_id, team2_id)
        return (season_id, week, team2_id, team1_id)

    def add(self, game: GameDto) -> None:
        key = self._get_key(
            game.season_id, game.week, game.home_team_id, game.away_team_id,
        )
        if key in self._by_key:
            raise ValueError(
                f"Game already exists for week {game.week} in season {game.season_id} between {game.home_team_id} and {game.away_team_id}",
            )

        self._by_id[game.id_] = game
        self._by_key[key] = game

        by_season = self._by_season.get(game.season_id)
        if by_season is None:
            by_season = []
            self._by_season[game.season_id] = by_season
        by_season.append(game)

    def get(self, id_: UUID) -> Optional[GameDto]:
        return self._by_id.get(id_)

    def find(
        self, season_id: UUID, week: int, team1_id: UUID, team2_id: UUID,
    ) -> Optional[GameDto]:
        key = self._get_key(season_id, week, team1_id, team2_id)
        return self._by_key.get(key)

    def for_season(self, season_id: UUID) -> List[GameDto]:
        by_season = self._by_season.get(season_id)
        if by_season is None:
            return []
        return list(by_season)

    def all(self) -> Iterable[GameDto]:
        return self._by_key.values()

    def drop(self) -> None:
        self._by_id = {}
        self._by_key = {}
        self._by_season = {}
