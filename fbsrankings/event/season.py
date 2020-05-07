from fbsrankings.common import Event
        

class SeasonRegisteredEvent (Event):
    def __init__(self, ID, year):
        self.ID = ID
        self.year = year
