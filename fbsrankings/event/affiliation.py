from fbsrankings.common import Event


class AffiliationCreatedEvent (Event):
    def __init__(self, ID, season_ID, team_ID, subdivision):
        self.ID = ID
        self.season_ID = season_ID
        self.team_ID = team_ID
        self.subdivision = subdivision
