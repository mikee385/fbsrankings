class ValidationError (ValueError):
    pass


class ValidationService (object):
    def validate_season(self, season, year):
        if season.year != year:
            raise ValidationError(f'Season.year does not match year: {season.year} vs. {year}')
            
    def validate_team(self, team, name):
        if team.name != name:
            raise ValidationError(f'Team.name does not match name: {team.name} vs. {name}')
            
    def validate_affiliation(self, affiliation, season_ID, team_ID, subdivision):
        if affiliation.season_ID != season_ID:
            raise ValidationError(f'Affiliation.season_ID does not match season_ID: {affiliation.season_ID} vs. {season_ID}')
        if affiliation.team_ID != team_ID:
            raise ValidationError(f'Affiliation.team_ID does not match team_ID: {affiliation.team_ID} vs. {team_ID}')
        if affiliation.subdivision != subdivision:
            raise ValidationError(f'Affiliation.subdivision does not match subdivision: {affiliation.subdivision} vs. {subdivision}')
            
    def validate_game(self, game, season_ID, week, date_, season_section, home_team_ID, away_team_ID, home_team_score, away_team_score, status, notes):
        if game.season_ID != season_ID:
            raise ValidationError(f'Game.season_ID does not match season_ID: {game.season_ID} vs. {season_ID}')
        if game.week != week:
            raise ValidationError(f'Game.week does not match week: {game.week} vs. {week}')
        if game.date != date_:
            raise ValidationError(f'Game.date does not match date: {game.date} vs. {date_}')
        if game.season_section != season_section:
            raise ValidationError(f'Game.season_section does not match season_section: {game.season_section} vs. {season_section}')
        if game.home_team_ID != home_team_ID:
            raise ValidationError(f'Game.home_team_ID does not match home_team_ID: {game.home_team_ID} vs. {home_team_ID}')
        if game.away_team_ID != away_team_ID:
            raise ValidationError(f'Game.away_team_ID does not match away_team_ID: {game.away_team_ID} vs. {away_team_ID}')
        if game.home_team_score != home_team_score:
            raise ValidationError(f'Game.home_team_score does not match home_team_score: {game.home_team_score} vs. {home_team_score}')
        if game.away_team_score != away_team_score:
            raise ValidationError(f'Game.away_team_score does not match away_team_score: {game.away_team_score} vs. {away_team_score}')
        if game.status != status:
            raise ValidationError(f'Game.status does not match status: {game.status} vs. {status}')
        if game.notes != notes:
            raise ValidationError(f'Game.notes does not match notes: {game.notes} vs. {notes}')
