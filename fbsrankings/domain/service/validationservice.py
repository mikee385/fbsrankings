class ValidationError (ValueError):
    pass

class ValidationService (object):
    def validate_season(self, season, year):
        if season.year != year:
            raise ValidationError('Season.year does not match year: {} vs. {}'.format(season.year, year))
            
    def validate_team(self, team, name):
        if team.name != name:
            raise ValidationError('Team.name does not match name: {} vs. {}'.format(team.name, name))
            
    def validate_affiliation(self, affiliation, season_ID, team_ID):
        if affiliation.season_ID != season_ID:
            raise ValidationError('Affiliation.season_ID does not match season_ID: {} vs. {}'.format(affiliation.season_ID, season_ID))
        if affiliation.team_ID != team_ID:
            raise ValidationError('Affiliation.team_ID does not match team_ID: {} vs. {}'.format(affiliation.team_ID, team_ID))
            
    def validate_game(self, game, season_ID, week, date_, season_section, home_team_ID, away_team_ID, home_team_score, away_team_score, notes):
        if game.season_ID != season_ID:
            raise ValidationError('Game.season_ID does not match season_ID: {} vs. {}'.format(game.season_ID, season_ID))
        if game.week != week:
            raise ValidationError('Game.week does not match week: {} vs. {}'.format(game.week, week))
        if game.date != date_:
            raise ValidationError('Game.date does not match date: {} vs. {}'.format(game.date, date))
        if game.season_section != season_section:
            raise ValidationError('Game.season_section does not match season_section: {} vs. {}'.format(game.season_section, season_section))
        if game.home_team_ID != home_team_ID:
            raise ValidationError('Game.home_team_ID does not match home_team_ID: {} vs. {}'.format(game.home_team_ID, home_team_ID))
        if game.away_team_ID != away_team_ID:
            raise ValidationError('Game.away_team_ID does not match away_team_ID: {} vs. {}'.format(game.away_team_ID, away_team_ID))
        if game.home_team_score != home_team_score:
            raise ValidationError('Game.home_team_score does not match home_team_score: {} vs. {}'.format(game.home_team_score, home_team_score))
        if game.away_team_score != away_team_score:
            raise ValidationError('Game.away_team_score does not match away_team_score: {} vs. {}'.format(game.away_team_score, away_team_score))
        if game.notes != notes:
            raise ValidationError('Game.notes does not match notes: {} vs. {}'.format(game.notes, notes))
