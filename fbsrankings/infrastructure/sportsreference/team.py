from fbsrankings.domain import TeamRepository as BaseRepository


class TeamRepository (BaseRepository):
    def __init__(self, parent, repository):
        self._parent = parent
        
        if not isinstance(repository, BaseRepository):
            raise TypeError('repository must be of type GameRepository')
        self._repository = repository

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
