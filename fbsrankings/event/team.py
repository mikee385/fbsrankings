from fbsrankings.common import Event


class TeamCreatedEvent (Event):
    def __init__(self, ID, name):
        self.ID = ID
        self.name = name
