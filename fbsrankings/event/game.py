from fbsrankings.common import Event


class GameScheduledEvent (Event):
    def __init__(self, ID, season_ID, week, date_, season_section, home_team_ID, away_team_ID, notes):
        self.ID = ID
        self.season_ID = season_ID
        self.week = week
        self.date = date_
        self.season_section = season_section
        self.home_team_ID = home_team_ID
        self.away_team_ID = away_team_ID
        self.notes = notes
    

class GameRescheduledEvent (Event):
    def __init__(self, ID, old_week, old_date, week, date_):
        self.ID = ID
        self.old_week = old_week
        self.old_date = old_date
        self.week = week
        self.date = date_
    

class GameCanceledEvent (Event):
    def __init__(self, ID):
        self.ID = ID
    

class GameCompletedEvent (Event):
    def __init__(self, ID, home_team_score, away_team_score):
        self.ID = ID
        self.home_team_score = home_team_score
        self.away_team_score = away_team_score
        

class GameNotesUpdatedEvent (Event):
    def __init__(self, ID, old_notes, notes):
        self.ID = ID
        self.old_notes = old_notes
        self.notes = notes
