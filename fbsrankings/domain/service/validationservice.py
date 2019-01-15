from enum import Enum

from fbsrankings.domain import Subdivision, GameStatus


class ValidationError (ValueError):
    pass
    

class MultipleValidationError (ValidationError):
    def __init__(self, errors):
        ValidationError.__init__(self, 'Multiple validation errors have occurred. See the errors property for more details.')
        self.errors = errors


class SeasonDataValidationError (ValidationError):
    def __init__(self, message, season_ID, attribute_name, attribute_value, expected_value):
        ValidationError.__init__(self, message)
        self.season_ID = season_ID
        self.attribute_name = attribute_name
        self.attribute_value = attribute_value
        self.expected_value = expected_value


class TeamDataValidationError (ValidationError):
    def __init__(self, message, team_ID, attribute_name, attribute_value, expected_value):
        ValidationError.__init__(self, message)
        self.team_ID = team_ID
        self.attribute_name = attribute_name
        self.attribute_value = attribute_value
        self.expected_value = expected_value


class AffiliationDataValidationError (ValidationError):
    def __init__(self, message, affiliation_ID, attribute_name, attribute_value, expected_value):
        ValidationError.__init__(self, message)
        self.affiliation_ID = affiliation_ID
        self.attribute_name = attribute_name
        self.attribute_value = attribute_value
        self.expected_value = expected_value


class GameDataValidationError (ValidationError):
    def __init__(self, message, game_ID, attribute_name, attribute_value, expected_value):
        ValidationError.__init__(self, message)
        self.game_ID = game_ID
        self.attribute_name = attribute_name
        self.attribute_value = attribute_value
        self.expected_value = expected_value


class DuplicateGameValidationError (ValidationError):
    def __init__(self, message, first_game_ID, second_game_ID):
        ValidationError.__init__(self, message)
        self.first_game_ID = first_game_ID
        self.second_game_ID = second_game_ID


class FBSGameCountValidationError (ValidationError):
    def __init__(self, message, team_ID, game_count):
        ValidationError.__init__(self, message)
        self.team_ID = team_ID
        self.game_count = game_count


class FCSGameCountValidationError (ValidationError):
    def __init__(self, message, team_ID, game_count):
        ValidationError.__init__(self, message)
        self.team_ID = team_ID
        self.game_count = game_count


class RaiseBehavior (Enum):
    IMMEDIATELY = 0
    ON_DEMAND = 1


class ValidationService (object):
    def __init__(self, raise_behavior=RaiseBehavior.IMMEDIATELY):
        self.raise_behavior = raise_behavior
        self.errors = []
    
    def validate_season_data(self, season, year):
        if season.year != year:
            self._handle_error(SeasonDataValidationError(f'Season.year does not match year: {season.year} vs. {year}', season.ID, 'year', season.year, year))
            
    def validate_team_data(self, team, name):
        if team.name != name:
            self._handle_error(TeamDataValidationError(f'Team.name does not match name: {team.name} vs. {name}', team.ID, 'name', team.name, name))
            
    def validate_affiliation_data(self, affiliation, season_ID, team_ID, subdivision):
        if affiliation.season_ID != season_ID:
            self._handle_error(AffiliationDataValidationError(f'Affiliation.season_ID does not match season_ID: {affiliation.season_ID} vs. {season_ID}', affiliation.ID, 'season_ID', affiliation.season_ID, season_ID))
        if affiliation.team_ID != team_ID:
            self._handle_error(AffiliationDataValidationError(f'Affiliation.team_ID does not match team_ID: {affiliation.team_ID} vs. {team_ID}', affiliation.ID, 'team_ID', affiliation.team_ID, team_ID))
        if affiliation.subdivision != subdivision:
            self._handle_error(AffiliationDataValidationError(f'Affiliation.subdivision does not match subdivision: {affiliation.subdivision} vs. {subdivision}', affiliation.ID, 'subdivision', affiliation.subdivision, subdivision))
            
    def validate_game_data(self, game, season_ID, week, date_, season_section, home_team_ID, away_team_ID, home_team_score, away_team_score, status, notes):
        if game.season_ID != season_ID:
            self._handle_error(GameDataValidationError(f'Game.season_ID does not match season_ID: {game.season_ID} vs. {season_ID}', game.ID, 'season_ID', game.season_ID, season_ID))
        if game.week != week:
            self._handle_error(GameDataValidationError(f'Game.week does not match week: {game.week} vs. {week}', game.ID, 'week', game.week, week))
        if game.date != date_:
            self._handle_error(GameDataValidationError(f'Game.date does not match date: {game.date} vs. {date_}', game.ID, 'date', game.date, date_))
        if game.season_section != season_section:
            self._handle_error(GameDataValidationError(f'Game.season_section does not match season_section: {game.season_section} vs. {season_section}', game.ID, 'season_section', game.season_section, season_section))
        if game.home_team_ID != home_team_ID:
            self._handle_error(GameDataValidationError(f'Game.home_team_ID does not match home_team_ID: {game.home_team_ID} vs. {home_team_ID}', game.ID, 'home_team_ID', game.home_team_ID, home_team_ID))
        if game.away_team_ID != away_team_ID:
            self._handle_error(GameDataValidationError(f'Game.away_team_ID does not match away_team_ID: {game.away_team_ID} vs. {away_team_ID}', game.ID, 'away_team_ID', game.away_team_ID, away_team_ID))
        if game.home_team_score != home_team_score:
            self._handle_error(GameDataValidationError(f'Game.home_team_score does not match home_team_score: {game.home_team_score} vs. {home_team_score}', game.ID, 'home_team_score', game.home_team_score, home_team_score))
        if game.away_team_score != away_team_score:
            self._handle_error(GameDataValidationError(f'Game.away_team_score does not match away_team_score: {game.away_team_score} vs. {away_team_score}', game.ID, 'away_team_score', game.away_team_score, away_team_score))
        if game.status != status:
            self._handle_error(GameDataValidationError(f'Game.status does not match status: {game.status} vs. {status}', game.ID, 'status', game.status, status))
        if game.notes != notes:
            self._handle_error(GameDataValidationError(f'Game.notes does not match notes: {game.notes} vs. {notes}', game.ID, 'notes', game.notes, notes))

    def validate_games(self, affiliations, games):
        fbs_game_counts = {}
        fcs_game_counts = {}
        for affiliation in affiliations:
            if affiliation.subdivision == Subdivision.FBS:
                fbs_game_counts[affiliation.team_ID] = 0
            elif affiliation.subdivision == Subdivision.FCS:
                fcs_game_counts[affiliation.team_ID] = 0
            else:
                self._handle_error(AffiliationDataValidationError(f'Unknown subdivision: {affiliation.subdivision}', affiliation.ID, 'subdivision', affiliation.subdivision, None))
        
        game_keys = {}
        for game in games:
            if game.home_team_ID < game.away_team_ID:
                key = (game.season_ID, game.season_section, game.home_team_ID, game.away_team_ID)
            else:
                key = (game.season_ID, game.season_section, game.away_team_ID, game.home_team_ID)
            if key in game_keys:
                self._handle_error(DuplicateGameValidationError('Duplicate games detected', game_keys[key].ID, game.ID))
            else:
                game_keys[key] = game
                
            if game.home_team_ID in fbs_game_counts:
                fbs_game_counts[game.home_team_ID] += 1
            elif game.home_team_ID in fcs_game_counts:
                fcs_game_counts[game.home_team_ID] += 1
            else:
                self._handle_error(GameDataValidationError('Unknown home team', game.ID, 'home_team_ID', game.home_team_ID, None))
            
            if game.away_team_ID in fbs_game_counts:
                fbs_game_counts[game.away_team_ID] += 1
            elif game.away_team_ID in fcs_game_counts:
                fcs_game_counts[game.away_team_ID] += 1
            else:
                self._handle_error(GameDataValidationError('Unknown away team', game.ID, 'away_team', game.away_team_ID, None))
        
        for team, game_count in fbs_game_counts.items():
            if game_count < 10:
                self._handle_error(FBSGameCountValidationError('FBS team has too few games', team, game_count))
                
        for team, game_count in fcs_game_counts.items():
            if game_count > 3:
                self._handle_error(FCSGameCountValidationError('FCS team had too many games', team, game_count))
                
    def raise_errors(self):
        if len(self.errors) == 1:
            error = self.errors[0]
            self.errors.clear()
            raise error
        elif len(self.errors) > 1:
            error = MultipleValidationError(self.errors)
            self.errors = []
            raise error
                
    def _handle_error(self, error):
        if self.raise_behavior == RaiseBehavior.IMMEDIATELY:
            raise error
        elif self.raise_behavior == RaiseBehavior.ON_DEMAND:
            self.errors.append(error)
