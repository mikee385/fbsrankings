from fbsrankings.domain import TeamRepository


class TeamQueryHandler (TeamRepository):
    def __init__(self, parent, repository):
        self._parent = parent
        
        if not isinstance(repository, TeamRepository):
            raise TypeError('repository must be of type GameRepository')
        self._repository = repository
        
        super().__init__(self._repository._event_bus)

    def find_by_ID(self, ID):
        return self._repository.find_by_ID(ID)
        
    def find_by_name(self, name):
        team = self._repository.find_by_name(name)
        if team is None:
            self._parent.load_all()
            team = self._repository.find_by_name(name)
        return team
    
    def all(self):
        self._parent.load_all()
        return self._repository.all()
