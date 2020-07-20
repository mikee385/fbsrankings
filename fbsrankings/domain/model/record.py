from abc import ABCMeta
from abc import abstractmethod
from typing import List
from typing import Optional
from typing import Sequence
from uuid import uuid4

from fbsrankings.common import EventBus
from fbsrankings.common import Identifier
from fbsrankings.domain.model.season import SeasonID
from fbsrankings.domain.model.team import TeamID
from fbsrankings.event import TeamRecordCalculatedEvent
from fbsrankings.event import TeamRecordValue as EventValue


class TeamRecordID(Identifier):
    pass


class TeamRecordValue(object):
    def __init__(self, team_ID: TeamID, wins: int, losses: int,) -> None:
        self._team_ID = team_ID
        self._wins = wins
        self._losses = losses

    @property
    def team_ID(self) -> TeamID:
        return self._team_ID

    @property
    def wins(self) -> int:
        return self._wins

    @property
    def losses(self) -> int:
        return self._losses

    @property
    def games(self) -> int:
        return self.wins + self.losses

    @property
    def win_percentage(self) -> float:
        return float(self.wins) / self.games if self.wins > 0 else 0.0


class TeamRecord(object):
    def __init__(
        self,
        bus: EventBus,
        ID: TeamRecordID,
        season_ID: SeasonID,
        week: Optional[int],
        values: List[TeamRecordValue],
    ) -> None:
        self._bus = bus
        self._ID = ID
        self._season_ID = season_ID
        self._week = week
        self._values = values

    @property
    def ID(self) -> TeamRecordID:
        return self._ID

    @property
    def season_ID(self) -> SeasonID:
        return self._season_ID

    @property
    def week(self) -> Optional[int]:
        return self._week

    @property
    def values(self) -> Sequence[TeamRecordValue]:
        return self._values


class TeamRecordRepository(metaclass=ABCMeta):
    def __init__(self, bus: EventBus) -> None:
        self._bus = bus

    def create(
        self, season_ID: SeasonID, week: Optional[int], values: List[TeamRecordValue],
    ) -> TeamRecord:
        ID = TeamRecordID(uuid4())
        record = TeamRecord(self._bus, ID, season_ID, week, values)
        self._bus.publish(
            TeamRecordCalculatedEvent(
                record.ID.value,
                record.season_ID.value,
                record.week,
                [
                    EventValue(
                        value.team_ID.value,
                        value.wins,
                        value.losses,
                        value.games,
                        value.win_percentage,
                    )
                    for value in record.values
                ],
            )
        )

        return record

    @abstractmethod
    def get(self, ID: TeamRecordID) -> Optional[TeamRecord]:
        raise NotImplementedError

    @abstractmethod
    def find(self, season_ID: SeasonID, week: Optional[int]) -> Optional[TeamRecord]:
        raise NotImplementedError
