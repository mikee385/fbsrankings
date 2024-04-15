import datetime
from typing import Optional

from fbsrankings.core.command.domain.model.affiliation import Affiliation
from fbsrankings.core.command.domain.model.factory import Factory
from fbsrankings.core.command.domain.model.game import Game
from fbsrankings.core.command.domain.model.season import Season
from fbsrankings.core.command.domain.model.season import SeasonID
from fbsrankings.core.command.domain.model.team import Team
from fbsrankings.core.command.domain.model.team import TeamID
from fbsrankings.core.command.infrastructure.repository import Repository
from fbsrankings.enum import GameStatus
from fbsrankings.enum import SeasonSection
from fbsrankings.enum import Subdivision


class Importer:
    def __init__(self, factory: Factory, repository: Repository) -> None:
        self._factory = factory
        self._repository = repository

    def import_season(self, year: int) -> Season:
        season = self._repository.season.find(year)
        if season is None:
            season = self._factory.season.create(year)

        return season

    def import_team(self, name: str) -> Team:
        team = self._repository.team.find(name)
        if team is None:
            team = self._factory.team.create(name)

        return team

    def import_affiliation(
        self,
        season_id: SeasonID,
        team_id: TeamID,
        subdivision: Subdivision,
    ) -> Affiliation:
        affiliation = self._repository.affiliation.find(season_id, team_id)
        if affiliation is None:
            affiliation = self._factory.affiliation.create(
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
            game = self._factory.game.create(
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
