import datetime
from enum import Enum
from typing import Iterable
from typing import List
from typing import Optional
from uuid import UUID

from fbsrankings.core.command.domain.model.affiliation import Affiliation
from fbsrankings.core.command.domain.model.game import Game
from fbsrankings.core.command.domain.model.season import Season
from fbsrankings.core.command.domain.model.season import SeasonID
from fbsrankings.core.command.domain.model.team import Team
from fbsrankings.core.command.domain.model.team import TeamID
from fbsrankings.enum import GameStatus
from fbsrankings.enum import SeasonSection
from fbsrankings.enum import Subdivision


class ValidationError(ValueError):
    pass


class MultipleValidationError(ValidationError):
    def __init__(self, errors: List[ValidationError]) -> None:
        super().__init__(
            "Multiple validation errors have occurred. See the errors property for"
            " more details.",
        )
        self.errors = errors


class SeasonDataValidationError(ValidationError):
    def __init__(
        self,
        message: str,
        season_id: UUID,
        attribute_name: str,
        attribute_value: object,
        expected_value: object,
    ) -> None:
        super().__init__(message)
        self.season_id = season_id
        self.attribute_name = attribute_name
        self.attribute_value = attribute_value
        self.expected_value = expected_value


class TeamDataValidationError(ValidationError):
    def __init__(
        self,
        message: str,
        team_id: UUID,
        attribute_name: str,
        attribute_value: object,
        expected_value: object,
    ) -> None:
        super().__init__(message)
        self.team_id = team_id
        self.attribute_name = attribute_name
        self.attribute_value = attribute_value
        self.expected_value = expected_value


class AffiliationDataValidationError(ValidationError):
    def __init__(
        self,
        message: str,
        affiliation_id: UUID,
        attribute_name: str,
        attribute_value: object,
        expected_value: object,
    ) -> None:
        super().__init__(message)
        self.affiliation_id = affiliation_id
        self.attribute_name = attribute_name
        self.attribute_value = attribute_value
        self.expected_value = expected_value


class GameDataValidationError(ValidationError):
    def __init__(
        self,
        message: str,
        game_id: UUID,
        attribute_name: str,
        attribute_value: object,
        expected_value: object,
    ) -> None:
        super().__init__(message)
        self.game_id = game_id
        self.attribute_name = attribute_name
        self.attribute_value = attribute_value
        self.expected_value = expected_value


class FBSGameCountValidationError(ValidationError):
    def __init__(
        self,
        message: str,
        season_id: UUID,
        team_id: UUID,
        game_count: int,
    ) -> None:
        super().__init__(message)
        self.season_id = season_id
        self.team_id = team_id
        self.game_count = game_count


class FCSGameCountValidationError(ValidationError):
    def __init__(
        self,
        message: str,
        season_id: UUID,
        team_id: UUID,
        game_count: int,
    ) -> None:
        super().__init__(message)
        self.season_id = season_id
        self.team_id = team_id
        self.game_count = game_count


class PostseasonGameCountValidationError(ValidationError):
    def __init__(
        self,
        message: str,
        season_id: UUID,
        regular_season_game_count: int,
        postseason_game_count: int,
    ) -> None:
        super().__init__(message)
        self.season_id = season_id
        self.regular_season_game_count = regular_season_game_count
        self.postseason_game_count = postseason_game_count


class RaiseBehavior(Enum):
    IMMEDIATELY = 0
    ON_DEMAND = 1


class ValidationService:
    def __init__(
        self,
        raise_behavior: RaiseBehavior = RaiseBehavior.IMMEDIATELY,
    ) -> None:
        self.raise_behavior = raise_behavior
        self.errors: List[ValidationError] = []

    def validate_season_data(self, season: Season, year: int) -> None:
        if season.year != year:
            self._handle_error(
                SeasonDataValidationError(
                    f"Season.year does not match year: {season.year} vs. {year}",
                    season.id_.value,
                    "year",
                    season.year,
                    year,
                ),
            )

    def validate_team_data(self, team: Team, name: str) -> None:
        if team.name != name:
            self._handle_error(
                TeamDataValidationError(
                    f"Team.name does not match name: {team.name} vs. {name}",
                    team.id_.value,
                    "name",
                    team.name,
                    name,
                ),
            )

    def validate_affiliation_data(
        self,
        affiliation: Affiliation,
        season_id: SeasonID,
        team_id: TeamID,
        subdivision: Subdivision,
    ) -> None:
        if affiliation.season_id != season_id:
            self._handle_error(
                AffiliationDataValidationError(
                    "Affiliation.season_id does not match season_id:"
                    f" {affiliation.season_id} vs. {season_id}",
                    affiliation.id_.value,
                    "season_id",
                    affiliation.season_id.value,
                    season_id.value,
                ),
            )
        if affiliation.team_id != team_id:
            self._handle_error(
                AffiliationDataValidationError(
                    "Affiliation.team_id does not match team_id:"
                    f" {affiliation.team_id} vs. {team_id}",
                    affiliation.id_.value,
                    "team_id",
                    affiliation.team_id.value,
                    team_id.value,
                ),
            )
        if affiliation.subdivision != subdivision:
            self._handle_error(
                AffiliationDataValidationError(
                    "Affiliation.subdivision does not match subdivision:"
                    f" {affiliation.subdivision} vs. {subdivision}",
                    affiliation.id_.value,
                    "subdivision",
                    affiliation.subdivision.name,
                    subdivision.name,
                ),
            )

    def validate_game_data(
        self,
        game: Game,
        season_id: SeasonID,
        week: int,
        date: datetime.date,
        season_section: SeasonSection,
        home_team_id: TeamID,
        away_team_id: TeamID,
        home_team_score: Optional[int],
        away_team_score: Optional[int],
        status: GameStatus,
        notes: str,
    ) -> None:
        if game.season_id != season_id:
            self._handle_error(
                GameDataValidationError(
                    f"Game.season_id does not match season_id: {game.season_id} vs."
                    f" {season_id}",
                    game.id_.value,
                    "season_id",
                    game.season_id.value,
                    season_id.value,
                ),
            )
        if game.week != week:
            self._handle_error(
                GameDataValidationError(
                    f"Game.week does not match week: {game.week} vs. {week}",
                    game.id_.value,
                    "week",
                    game.week,
                    week,
                ),
            )
        if game.date != date:
            self._handle_error(
                GameDataValidationError(
                    f"Game.date does not match date: {game.date} vs. {date}",
                    game.id_.value,
                    "date",
                    game.date,
                    date,
                ),
            )
        if game.season_section != season_section:
            self._handle_error(
                GameDataValidationError(
                    "Game.season_section does not match season_section:"
                    f" {game.season_section} vs. {season_section}",
                    game.id_.value,
                    "season_section",
                    game.season_section.name,
                    season_section.name,
                ),
            )
        if game.home_team_id != home_team_id:
            self._handle_error(
                GameDataValidationError(
                    "Game.home_team_id does not match home_team_id:"
                    f" {game.home_team_id} vs. {home_team_id}",
                    game.id_.value,
                    "home_team_id",
                    game.home_team_id.value,
                    home_team_id.value,
                ),
            )
        if game.away_team_id != away_team_id:
            self._handle_error(
                GameDataValidationError(
                    "Game.away_team_id does not match away_team_id:"
                    f" {game.away_team_id} vs. {away_team_id}",
                    game.id_.value,
                    "away_team_id",
                    game.away_team_id.value,
                    away_team_id.value,
                ),
            )
        if game.home_team_score != home_team_score:
            self._handle_error(
                GameDataValidationError(
                    "Game.home_team_score does not match home_team_score:"
                    f" {game.home_team_score} vs. {home_team_score}",
                    game.id_.value,
                    "home_team_score",
                    game.home_team_score,
                    home_team_score,
                ),
            )
        if game.away_team_score != away_team_score:
            self._handle_error(
                GameDataValidationError(
                    "Game.away_team_score does not match away_team_score:"
                    f" {game.away_team_score} vs. {away_team_score}",
                    game.id_.value,
                    "away_team_score",
                    game.away_team_score,
                    away_team_score,
                ),
            )

        winning_team_id: Optional[TeamID]
        losing_team_id: Optional[TeamID]
        winning_team_score: Optional[int]
        losing_team_score: Optional[int]
        if home_team_score is not None and away_team_score is not None:
            if home_team_score > away_team_score:
                winning_team_id = home_team_id
                losing_team_id = away_team_id
                winning_team_score = home_team_score
                losing_team_score = away_team_score
            else:
                winning_team_id = away_team_id
                losing_team_id = home_team_id
                winning_team_score = away_team_score
                losing_team_score = home_team_score
        else:
            winning_team_id = None
            losing_team_id = None
            winning_team_score = None
            losing_team_score = None

        if game.winning_team_id != winning_team_id:
            self._handle_error(
                GameDataValidationError(
                    "Game.winning_team_id does not match winning_team_id:"
                    f" {game.winning_team_id} vs. {winning_team_id}",
                    game.id_.value,
                    "winning_team_id",
                    game.winning_team_id.value
                    if game.winning_team_id is not None
                    else None,
                    winning_team_id.value if winning_team_id is not None else None,
                ),
            )
        if game.losing_team_id != losing_team_id:
            self._handle_error(
                GameDataValidationError(
                    "Game.losing_team_id does not match losing_team_id:"
                    f" {game.losing_team_id} vs. {losing_team_id}",
                    game.id_.value,
                    "losing_team_id",
                    game.losing_team_id.value
                    if game.losing_team_id is not None
                    else None,
                    losing_team_id.value if losing_team_id is not None else None,
                ),
            )
        if game.winning_team_score != winning_team_score:
            self._handle_error(
                GameDataValidationError(
                    "Game.winning_team_score does not match winning_team_score:"
                    f" {game.winning_team_score} vs. {winning_team_score}",
                    game.id_.value,
                    "winning_team_score",
                    game.winning_team_score,
                    winning_team_score,
                ),
            )
        if game.losing_team_score != losing_team_score:
            self._handle_error(
                GameDataValidationError(
                    "Game.losing_team_score does not match losing_team_score:"
                    f" {game.losing_team_score} vs. {losing_team_score}",
                    game.id_.value,
                    "losing_team_score",
                    game.losing_team_score,
                    losing_team_score,
                ),
            )
        if game.status != status:
            self._handle_error(
                GameDataValidationError(
                    f"Game.status does not match status: {game.status} vs. {status}",
                    game.id_.value,
                    "status",
                    game.status.name,
                    status.name,
                ),
            )
        if game.notes != notes:
            self._handle_error(
                GameDataValidationError(
                    f"Game.notes does not match notes: {game.notes} vs. {notes}",
                    game.id_.value,
                    "notes",
                    game.notes,
                    notes,
                ),
            )

    def validate_season_games(
        self,
        season_id: SeasonID,
        affiliations: Iterable[Affiliation],
        games: Iterable[Game],
    ) -> None:
        fbs_game_counts = {}
        fcs_game_counts = {}
        for affiliation in affiliations:
            if affiliation.subdivision == Subdivision.FBS:
                fbs_game_counts[affiliation.team_id] = 0
            elif affiliation.subdivision == Subdivision.FCS:
                fcs_game_counts[affiliation.team_id] = 0
            else:
                self._handle_error(
                    AffiliationDataValidationError(
                        f"Unknown subdivision: {affiliation.subdivision}",
                        affiliation.id_.value,
                        "subdivision",
                        affiliation.subdivision.name,
                        None,
                    ),
                )

        regular_season_game_count = 0
        postseason_game_count = 0

        for game in games:
            if game.home_team_id in fbs_game_counts:
                fbs_game_counts[game.home_team_id] += 1
            elif game.home_team_id in fcs_game_counts:
                fcs_game_counts[game.home_team_id] += 1
            else:
                self._handle_error(
                    GameDataValidationError(
                        "Unknown home team",
                        game.id_.value,
                        "home_team_id",
                        game.home_team_id.value,
                        None,
                    ),
                )

            if game.away_team_id in fbs_game_counts:
                fbs_game_counts[game.away_team_id] += 1
            elif game.away_team_id in fcs_game_counts:
                fcs_game_counts[game.away_team_id] += 1
            else:
                self._handle_error(
                    GameDataValidationError(
                        "Unknown away team",
                        game.id_.value,
                        "away_team",
                        game.away_team_id.value,
                        None,
                    ),
                )

            if game.season_section == SeasonSection.REGULAR_SEASON:
                regular_season_game_count += 1
            elif game.season_section == SeasonSection.POSTSEASON:
                postseason_game_count += 1

        for team_id, game_count in fbs_game_counts.items():
            if game_count < 10:
                self._handle_error(
                    FBSGameCountValidationError(
                        "FBS team has too few games",
                        season_id.value,
                        team_id.value,
                        game_count,
                    ),
                )

        for team_id, game_count in fcs_game_counts.items():
            if game_count > 5:
                self._handle_error(
                    FCSGameCountValidationError(
                        "FCS team had too many games",
                        season_id.value,
                        team_id.value,
                        game_count,
                    ),
                )

        postseason_percentage = float(postseason_game_count) / regular_season_game_count
        if postseason_percentage < 0.03:
            self._handle_error(
                PostseasonGameCountValidationError(
                    "Too few postseason games",
                    season_id.value,
                    regular_season_game_count,
                    postseason_game_count,
                ),
            )
        elif postseason_percentage > 0.06:
            self._handle_error(
                PostseasonGameCountValidationError(
                    "Too many postseason games",
                    season_id.value,
                    regular_season_game_count,
                    postseason_game_count,
                ),
            )

    def raise_errors(self) -> None:
        if len(self.errors) == 1:
            error = self.errors[0]
            self.errors.clear()
            raise error
        if len(self.errors) > 1:
            error = MultipleValidationError(self.errors)
            self.errors = []
            raise error

    def _handle_error(self, error: ValidationError) -> None:
        if self.raise_behavior == RaiseBehavior.IMMEDIATELY:
            raise error
        if self.raise_behavior == RaiseBehavior.ON_DEMAND:
            self.errors.append(error)
