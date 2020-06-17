from fbsrankings.common import Query


class CanceledGamesQuery (Query):
    pass
    
    
class CanceledGamesResult (object):
    def __init__(self, games):
        self.games = games
        

class CanceledGameResult (object):
    def __init__(self, ID, season_ID, year, week, date_, season_section, home_team_ID, home_team_name, away_team_ID, away_team_name, notes):
        self.ID = ID
        self.season_ID = season_ID
        self.year = year
        self.week = week
        self.date = date_
        self.season_section = season_section
        self.home_team_ID = home_team_ID
        self.home_team_name = home_team_name
        self.away_team_ID = away_team_ID
        self.away_team_name = away_team_name
        self.notes = notes
