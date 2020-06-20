from uuid import UUID

from fbsrankings.common import Event


class AffiliationCreatedEvent (Event):
    def __init__(self, ID: UUID, season_ID: UUID, team_ID: UUID, subdivision: str) -> None:
        self.ID = ID
        self.season_ID = season_ID
        self.team_ID = team_ID
        self.subdivision = subdivision
