from typing import List

from communication.messages import Event


class ValidationError(Event):
    def __init__(self, event_id: str, message: str) -> None:
        super().__init__()
        self.event_id = event_id
        self.message = message


class MultipleValidationError(ValidationError):
    def __init__(self, event_id: str, errors: List[ValidationError]) -> None:
        super().__init__(
            event_id,
            "Multiple validation errors have occurred. See the errors property for"
            " more details.",
        )
        self.errors = errors


class SeasonDataValidationError(ValidationError):
    def __init__(
        self,
        event_id: str,
        message: str,
        season_id: str,
        attribute_name: str,
        attribute_value: object,
        expected_value: object,
    ) -> None:
        super().__init__(event_id, message)
        self.season_id = season_id
        self.attribute_name = attribute_name
        self.attribute_value = attribute_value
        self.expected_value = expected_value


class TeamDataValidationError(ValidationError):
    def __init__(
        self,
        event_id: str,
        message: str,
        team_id: str,
        attribute_name: str,
        attribute_value: object,
        expected_value: object,
    ) -> None:
        super().__init__(event_id, message)
        self.team_id = team_id
        self.attribute_name = attribute_name
        self.attribute_value = attribute_value
        self.expected_value = expected_value


class AffiliationDataValidationError(ValidationError):
    def __init__(
        self,
        event_id: str,
        message: str,
        affiliation_id: str,
        attribute_name: str,
        attribute_value: object,
        expected_value: object,
    ) -> None:
        super().__init__(event_id, message)
        self.affiliation_id = affiliation_id
        self.attribute_name = attribute_name
        self.attribute_value = attribute_value
        self.expected_value = expected_value


class GameDataValidationError(ValidationError):
    def __init__(
        self,
        event_id: str,
        message: str,
        game_id: str,
        attribute_name: str,
        attribute_value: object,
        expected_value: object,
    ) -> None:
        super().__init__(event_id, message)
        self.game_id = game_id
        self.attribute_name = attribute_name
        self.attribute_value = attribute_value
        self.expected_value = expected_value


class FBSGameCountValidationError(ValidationError):
    def __init__(
        self,
        event_id: str,
        message: str,
        season_id: str,
        team_id: str,
        game_count: int,
    ) -> None:
        super().__init__(event_id, message)
        self.season_id = season_id
        self.team_id = team_id
        self.game_count = game_count


class FCSGameCountValidationError(ValidationError):
    def __init__(
        self,
        event_id: str,
        message: str,
        season_id: str,
        team_id: str,
        game_count: int,
    ) -> None:
        super().__init__(event_id, message)
        self.season_id = season_id
        self.team_id = team_id
        self.game_count = game_count


class PostseasonGameCountValidationError(ValidationError):
    def __init__(
        self,
        event_id: str,
        message: str,
        season_id: str,
        regular_season_game_count: int,
        postseason_game_count: int,
    ) -> None:
        super().__init__(event_id, message)
        self.season_id = season_id
        self.regular_season_game_count = regular_season_game_count
        self.postseason_game_count = postseason_game_count
