import datetime

from enum import Enum
from typing import Any, Iterable, List, Optional
from uuid import UUID

from fbsrankings.domain import Season, SeasonID, Team, TeamID, Affiliation, Game, SeasonSection, Subdivision, GameStatus


class ValidationError (ValueError):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class MultipleValidationError (ValidationError):
    def __init__(self, errors: List[ValidationError]) -> None:
        super().__init__('Multiple validation errors have occurred. See the errors property for more details.')
        self.errors = errors


class SeasonDataValidationError (ValidationError):
    def __init__(self, message: str, season_ID: UUID, attribute_name: str, attribute_value: Any, expected_value: Any) -> None:
        super().__init__(message)
        self.season_ID = season_ID
        self.attribute_name = attribute_name
        self.attribute_value = attribute_value
        self.expected_value = expected_value


class TeamDataValidationError (ValidationError):
    def __init__(self, message: str, team_ID: UUID, attribute_name: str, attribute_value: Any, expected_value: Any) -> None:
        super().__init__(message)
        self.team_ID = team_ID
        self.attribute_name = attribute_name
        self.attribute_value = attribute_value
        self.expected_value = expected_value


class AffiliationDataValidationError (ValidationError):
    def __init__(self, message: str, affiliation_ID: UUID, attribute_name: str, attribute_value: Any, expected_value: Any) -> None:
        super().__init__(message)
        self.affiliation_ID = affiliation_ID
        self.attribute_name = attribute_name
        self.attribute_value = attribute_value
        self.expected_value = expected_value


class GameDataValidationError (ValidationError):
    def __init__(self, message: str, game_ID: UUID, attribute_name: str, attribute_value: Any, expected_value: Any) -> None:
        super().__init__(message)
        self.game_ID = game_ID
        self.attribute_name = attribute_name
        self.attribute_value = attribute_value
        self.expected_value = expected_value


class FBSGameCountValidationError (ValidationError):
    def __init__(self, message: str, season_ID: UUID, team_ID: UUID, game_count: int) -> None:
        super().__init__(message)
        self.season_ID = season_ID
        self.team_ID = team_ID
        self.game_count = game_count


class FCSGameCountValidationError (ValidationError):
    def __init__(self, message: str, season_ID: UUID, team_ID: UUID, game_count: int) -> None:
        super().__init__(message)
        self.season_ID = season_ID
        self.team_ID = team_ID
        self.game_count = game_count


class RaiseBehavior (Enum):
    IMMEDIATELY = 0
    ON_DEMAND = 1


class ValidationService (object):
    def __init__(self, raise_behavior: RaiseBehavior=RaiseBehavior.IMMEDIATELY) -> None:
        self.raise_behavior: RaiseBehavior = raise_behavior
        self.errors: List[ValidationError] = []
    
    def validate_season_data(self, season: Season, year: int) -> None:
        if season.year != year:
            self._handle_error(SeasonDataValidationError(f'Season.year does not match year: {season.year} vs. {year}', season.ID.value, 'year', season.year, year))
            
    def validate_team_data(self, team: Team, name: str) -> None:
        if team.name != name:
            self._handle_error(TeamDataValidationError(f'Team.name does not match name: {team.name} vs. {name}', team.ID.value, 'name', team.name, name))
            
    def validate_affiliation_data(self, affiliation: Affiliation, season_ID: SeasonID, team_ID: TeamID, subdivision: Subdivision) -> None:
        if affiliation.season_ID != season_ID:
            self._handle_error(AffiliationDataValidationError(f'Affiliation.season_ID does not match season_ID: {affiliation.season_ID} vs. {season_ID}', affiliation.ID.value, 'season_ID', affiliation.season_ID.value, season_ID.value))
        if affiliation.team_ID != team_ID:
            self._handle_error(AffiliationDataValidationError(f'Affiliation.team_ID does not match team_ID: {affiliation.team_ID} vs. {team_ID}', affiliation.ID.value, 'team_ID', affiliation.team_ID.value, team_ID.value))
        if affiliation.subdivision != subdivision:
            self._handle_error(AffiliationDataValidationError(f'Affiliation.subdivision does not match subdivision: {affiliation.subdivision} vs. {subdivision}', affiliation.ID.value, 'subdivision', affiliation.subdivision.name, subdivision.name))
            
    def validate_game_data(self, game: Game, season_ID: SeasonID, week: int, date: datetime.date, season_section: SeasonSection, home_team_ID: TeamID, away_team_ID: TeamID, home_team_score: Optional[int], away_team_score: Optional[int], status: GameStatus, notes: str) -> None:
        if game.season_ID != season_ID:
            self._handle_error(GameDataValidationError(f'Game.season_ID does not match season_ID: {game.season_ID} vs. {season_ID}', game.ID.value, 'season_ID', game.season_ID.value, season_ID.value))
        if game.week != week:
            self._handle_error(GameDataValidationError(f'Game.week does not match week: {game.week} vs. {week}', game.ID.value, 'week', game.week, week))
        if game.date != date:
            self._handle_error(GameDataValidationError(f'Game.date does not match date: {game.date} vs. {date}', game.ID.value, 'date', game.date, date))
        if game.season_section != season_section:
            self._handle_error(GameDataValidationError(f'Game.season_section does not match season_section: {game.season_section} vs. {season_section}', game.ID.value, 'season_section', game.season_section.name, season_section.name))
        if game.home_team_ID != home_team_ID:
            self._handle_error(GameDataValidationError(f'Game.home_team_ID does not match home_team_ID: {game.home_team_ID} vs. {home_team_ID}', game.ID.value, 'home_team_ID', game.home_team_ID.value, home_team_ID.value))
        if game.away_team_ID != away_team_ID:
            self._handle_error(GameDataValidationError(f'Game.away_team_ID does not match away_team_ID: {game.away_team_ID} vs. {away_team_ID}', game.ID.value, 'away_team_ID', game.away_team_ID.value, away_team_ID.value))
        if game.home_team_score != home_team_score:
            self._handle_error(GameDataValidationError(f'Game.home_team_score does not match home_team_score: {game.home_team_score} vs. {home_team_score}', game.ID.value, 'home_team_score', game.home_team_score, home_team_score))
        if game.away_team_score != away_team_score:
            self._handle_error(GameDataValidationError(f'Game.away_team_score does not match away_team_score: {game.away_team_score} vs. {away_team_score}', game.ID.value, 'away_team_score', game.away_team_score, away_team_score))
        if game.status != status:
            self._handle_error(GameDataValidationError(f'Game.status does not match status: {game.status} vs. {status}', game.ID.value, 'status', game.status.name, status.name))
        if game.notes != notes:
            self._handle_error(GameDataValidationError(f'Game.notes does not match notes: {game.notes} vs. {notes}', game.ID.value, 'notes', game.notes, notes))

    def validate_season_games(self, season_ID: SeasonID, affiliations: Iterable[Affiliation], games: Iterable[Game]) -> None:
        fbs_game_counts = {}
        fcs_game_counts = {}
        for affiliation in affiliations:
            if affiliation.subdivision == Subdivision.FBS:
                fbs_game_counts[affiliation.team_ID] = 0
            elif affiliation.subdivision == Subdivision.FCS:
                fcs_game_counts[affiliation.team_ID] = 0
            else:
                self._handle_error(AffiliationDataValidationError(f'Unknown subdivision: {affiliation.subdivision}', affiliation.ID.value, 'subdivision', affiliation.subdivision.name, None))
        
        for game in games:
            if game.home_team_ID in fbs_game_counts:
                fbs_game_counts[game.home_team_ID] += 1
            elif game.home_team_ID in fcs_game_counts:
                fcs_game_counts[game.home_team_ID] += 1
            else:
                self._handle_error(GameDataValidationError('Unknown home team', game.ID.value, 'home_team_ID', game.home_team_ID.value, None))
            
            if game.away_team_ID in fbs_game_counts:
                fbs_game_counts[game.away_team_ID] += 1
            elif game.away_team_ID in fcs_game_counts:
                fcs_game_counts[game.away_team_ID] += 1
            else:
                self._handle_error(GameDataValidationError('Unknown away team', game.ID.value, 'away_team', game.away_team_ID.value, None))
        
        for team_ID, game_count in fbs_game_counts.items():
            if game_count < 10:
                self._handle_error(FBSGameCountValidationError('FBS team has too few games', season_ID.value, team_ID.value, game_count))

        for team_ID, game_count in fcs_game_counts.items():
            if game_count > 5:
                self._handle_error(FCSGameCountValidationError('FCS team had too many games', season_ID.value, team_ID.value, game_count))
                
    def raise_errors(self) -> None:
        if len(self.errors) == 1:
            error = self.errors[0]
            self.errors.clear()
            raise error
        elif len(self.errors) > 1:
            error = MultipleValidationError(self.errors)
            self.errors = []
            raise error
                
    def _handle_error(self, error: ValidationError) -> None:
        if self.raise_behavior == RaiseBehavior.IMMEDIATELY:
            raise error
        elif self.raise_behavior == RaiseBehavior.ON_DEMAND:
            self.errors.append(error)
