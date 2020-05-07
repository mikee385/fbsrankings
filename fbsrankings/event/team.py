from fbsrankings.common import Event


class TeamRegisteredEvent (Event):
    def __init__(self, ID, name):
        self.ID = ID
        self.name = name
