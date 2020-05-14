from fbsrankings.domain import SeasonRepository as BaseRepository


class SeasonRepository (BaseRepository):
    def __init__(self, parent, repository):
        self._parent = parent
        
        if not isinstance(repository, BaseRepository):
            raise TypeError('repository must be of type GameRepository')
        self._repository = repository

    def find_by_ID(self, ID):
        return self._repository.find_by_ID(ID)
        
    def find_by_year(self, year):
        return self._repository.find_by_year(year)
        
    def all(self):
        return self._repository.all()
