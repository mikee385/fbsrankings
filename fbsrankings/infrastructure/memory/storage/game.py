import datetime
from typing import Dict, Iterable, List, Optional, Tuple
from uuid import UUID


class GameDto(object):
    def __init__(
        self,
        ID: UUID,
        season_ID: UUID,
        week: int,
        date: datetime.date,
        season_section: str,
        home_team_ID: UUID,
        away_team_ID: UUID,
        home_team_score: Optional[int],
        away_team_score: Optional[int],
        status: str,
        notes: str,
    ) -> None:
        self.ID = ID
        self.season_ID = season_ID
        self.week = week
        self.date = date
        self.season_section = season_section
        self.home_team_ID = home_team_ID
        self.away_team_ID = away_team_ID
        self.home_team_score = home_team_score
        self.away_team_score = away_team_score
        self.status = status
        self.notes = notes


class GameStorage(object):
    def __init__(self) -> None:
        self._by_ID: Dict[UUID, GameDto] = {}
        self._by_key: Dict[Tuple[UUID, int, UUID, UUID], GameDto] = {}
        self._by_season: Dict[UUID, List[GameDto]] = {}

    def add(self, game: GameDto) -> None:
        key = self._get_key(
            game.season_ID, game.week, game.home_team_ID, game.away_team_ID
        )
        if key in self._by_key:
            raise ValueError(
                f"Game already exists for week {game.week} in season {game.season_ID} between {game.home_team_ID} and {game.away_team_ID}"
            )

        self._by_ID[game.ID] = game
        self._by_key[key] = game

        by_season = self._by_season.get(game.season_ID)
        if by_season is None:
            by_season = []
            self._by_season[game.season_ID] = by_season
        by_season.append(game)

    def get(self, ID: UUID) -> Optional[GameDto]:
        return self._by_ID.get(ID)

    def find(
        self, season_ID: UUID, week: int, team1_ID: UUID, team2_ID: UUID
    ) -> Optional[GameDto]:
        key = self._get_key(season_ID, week, team1_ID, team2_ID)
        return self._by_key.get(key)

    def by_season(self, season_ID: UUID) -> List[GameDto]:
        by_season = self._by_season.get(season_ID)
        if by_season is None:
            return []
        return list(by_season)

    def all(self) -> Iterable[GameDto]:
        return self._by_key.values()

    def _get_key(
        self, season_ID: UUID, week: int, team1_ID: UUID, team2_ID: UUID
    ) -> Tuple[UUID, int, UUID, UUID]:
        if team1_ID < team2_ID:
            return (season_ID, week, team1_ID, team2_ID)
        else:
            return (season_ID, week, team2_ID, team1_ID)
