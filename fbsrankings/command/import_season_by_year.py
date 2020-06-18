from fbsrankings.common import Command


class ImportSeasonByYearCommand (Command):
    def __init__(self, year):
        self.year = year
