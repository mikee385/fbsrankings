import datetime
from abc import ABCMeta
from abc import abstractmethod
from typing import Dict
from typing import Optional
from typing import Tuple

from typing_extensions import Protocol

from fbsrankings.domain.model.affiliation import Affiliation
from fbsrankings.domain.model.affiliation import AffiliationRepository
from fbsrankings.domain.model.affiliation import Subdivision
from fbsrankings.domain.model.game import Game
from fbsrankings.domain.model.game import GameRepository
from fbsrankings.domain.model.game import GameStatus
from fbsrankings.domain.model.season import Season
from fbsrankings.domain.model.season import SeasonID
from fbsrankings.domain.model.season import SeasonRepository
from fbsrankings.domain.model.season import SeasonSection
from fbsrankings.domain.model.team import Team
from fbsrankings.domain.model.team import TeamID
from fbsrankings.domain.model.team import TeamRepository


class RepositoryManager(Protocol, metaclass=ABCMeta):
    @property
    @abstractmethod
    def season(self) -> SeasonRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def team(self) -> TeamRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def affiliation(self) -> AffiliationRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def game(self) -> GameRepository:
        raise NotImplementedError


_SeasonCache = Dict[int, Season]
_TeamCache = Dict[str, Team]
_AffiliationCache = Dict[Tuple[SeasonID, TeamID], Affiliation]
_GameCache = Dict[Tuple[SeasonID, int, TeamID, TeamID], Game]


class _Cache:
    def __init__(self) -> None:
        self.season: _SeasonCache = {}
        self.team: _TeamCache = {}
        self.affiliation: _AffiliationCache = {}
        self.game: _GameCache = {}


class ImportService:
    def __init__(self, repository: RepositoryManager) -> None:
        self._repository = repository
        self._cache = _Cache()

    def import_season(self, year: int) -> Season:
        key = year

        season = self._cache.season.get(key)
        if season is None:
            season = self._repository.season.find(year)
            if season is None:
                season = self._repository.season.create(year)
            self._cache.season[key] = season

        return season

    def import_team(self, name: str) -> Team:
        key = name

        team = self._cache.team.get(key)
        if team is None:
            team = self._repository.team.find(name)
            if team is None:
                team = self._repository.team.create(name)
            self._cache.team[key] = team

        return team

    def import_affiliation(
        self,
        season_id: SeasonID,
        team_id: TeamID,
        subdivision: Subdivision,
    ) -> Affiliation:
        key = (season_id, team_id)

        affiliation = self._cache.affiliation.get(key)
        if affiliation is None:
            affiliation = self._repository.affiliation.find(season_id, team_id)
            if affiliation is None:
                affiliation = self._repository.affiliation.create(
                    season_id,
                    team_id,
                    subdivision,
                )
            self._cache.affiliation[key] = affiliation

        return affiliation

    def import_game(
        self,
        season_id: SeasonID,
        week: int,
        date: datetime.date,
        season_section: SeasonSection,
        home_team_id: TeamID,
        away_team_id: TeamID,
        home_team_score: Optional[int],
        away_team_score: Optional[int],
        notes: str,
    ) -> Game:
        if home_team_id < away_team_id:
            key = (season_id, week, home_team_id, away_team_id)
        else:
            key = (season_id, week, away_team_id, home_team_id)

        game = self._cache.game.get(key)
        if game is None:
            game = self._repository.game.find(
                season_id,
                week,
                home_team_id,
                away_team_id,
            )
            if game is None:
                game = self._repository.game.create(
                    season_id,
                    week,
                    date,
                    season_section,
                    home_team_id,
                    away_team_id,
                    notes,
                )
            self._cache.game[key] = game

        if date != game.date:
            game.reschedule(week, date)

        if (
            home_team_score is not None
            and away_team_score is not None
            and game.status != GameStatus.COMPLETED
        ):
            game.complete(home_team_score, away_team_score)

        if notes != game.notes:
            game.update_notes(notes)

        return game
