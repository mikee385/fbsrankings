from uuid import UUID

from fbsrankings.common import Event


class AffiliationCreatedEvent(Event):
    def __init__(
        self, id_: UUID, season_id: UUID, team_id: UUID, subdivision: str,
    ) -> None:
        self.id_ = id_
        self.season_id = season_id
        self.team_id = team_id
        self.subdivision = subdivision