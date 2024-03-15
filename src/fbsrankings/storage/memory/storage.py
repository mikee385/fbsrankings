from types import TracebackType
from typing import ContextManager
from typing import Optional
from typing import Type

from typing_extensions import Literal

from fbsrankings.storage.memory.affiliation import AffiliationStorage
from fbsrankings.storage.memory.game import GameStorage
from fbsrankings.storage.memory.ranking import RankingStorage
from fbsrankings.storage.memory.record import TeamRecordStorage
from fbsrankings.storage.memory.season import SeasonStorage
from fbsrankings.storage.memory.team import TeamStorage


class Storage(ContextManager["Storage"]):
    def __init__(self) -> None:
        self.season = SeasonStorage()
        self.team = TeamStorage()
        self.affiliation = AffiliationStorage()
        self.game = GameStorage()

        self.team_record = TeamRecordStorage()
        self.team_ranking = RankingStorage()
        self.game_ranking = RankingStorage()

    def drop(self) -> None:
        self.season.drop()
        self.team.drop()
        self.affiliation.drop()
        self.game.drop()

        self.team_record.drop()
        self.team_ranking.drop()
        self.game_ranking.drop()

    def close(self) -> None:
        pass

    def __enter__(self) -> "Storage":
        return self

    def __exit__(
        self,
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        return False
