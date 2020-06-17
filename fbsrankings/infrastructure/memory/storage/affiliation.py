class AffiliationDto (object):
    def __init__(self, ID, season_ID, team_ID, subdivision):
        self.ID = ID
        self.season_ID = season_ID
        self.team_ID = team_ID
        self.subdivision = subdivision


class AffiliationStorage (object):
    def __init__(self):
        self._affiliation_id_dict = {}
        self._affiliation_season_dict = {}
    
    def add(self, affiliation):
        if not isinstance(affiliation, AffiliationDto):
            raise TypeError('affiliation must be of type AffiliationDto')
        
        season_dict = self._affiliation_season_dict.get(affiliation.season_ID)
        if season_dict is None:
            season_dict = {}
            self._affiliation_season_dict[affiliation.season_ID] = season_dict
        elif affiliation.team_ID in season_dict:
            raise ValueError(f'Affiliation already exists for team {affiliation.team_ID} in season {affiliation.season_ID}')
        season_dict[affiliation.team_ID] = affiliation
        self._affiliation_id_dict[affiliation.ID] = affiliation

    def find_by_ID(self, ID):
        return self._affiliation_id_dict.get(ID)
        
    def find_by_season_team(self, season_ID, team_ID):
        season_dict = self._affiliation_season_dict.get(season_ID)
        if season_dict is None:
            return None
        return season_dict.get(team_ID)
        
    def find_by_season(self, season_ID):
        season_dict = self._affiliation_season_dict.get(season_ID)
        if season_dict is None:
            return []
        return [item for item in season_dict.values()]
