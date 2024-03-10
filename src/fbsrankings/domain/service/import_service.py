import datetime
from abc import ABCMeta
from abc import abstractmethod
from typing import Optional

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


class ImportService:
    def __init__(self, repository: RepositoryManager) -> None:
        self._repository = repository

    def import_season(self, year: int) -> Season:
        season = self._repository.season.find(year)
        if season is None:
            season = self._repository.season.create(year)

        return season

    def import_team(self, name: str) -> Team:
        team = self._repository.team.find(name)
        if team is None:
            team = self._repository.team.create(name)

        return team

    def import_affiliation(
        self,
        season_id: SeasonID,
        team_id: TeamID,
        subdivision: Subdivision,
    ) -> Affiliation:
        affiliation = self._repository.affiliation.find(season_id, team_id)
        if affiliation is None:
            affiliation = self._repository.affiliation.create(
                season_id,
                team_id,
                subdivision,
            )

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
