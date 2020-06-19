from fbsrankings.common import Event
        

class SeasonCreatedEvent (Event):
    def __init__(self, ID, year):
        self.ID = ID
        self.year = year
