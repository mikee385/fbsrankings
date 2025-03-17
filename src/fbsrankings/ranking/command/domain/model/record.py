from abc import ABCMeta
from abc import abstractmethod
from collections.abc import Sequence
from typing import NewType
from typing import Optional
from uuid import UUID
from uuid import uuid4

from communication.bus import EventBus
from fbsrankings.messages.event import TeamRecordCalculatedEvent
from fbsrankings.messages.event import TeamRecordValue as EventValue
from fbsrankings.ranking.command.domain.model.core import SeasonID
from fbsrankings.ranking.command.domain.model.core import TeamID


TeamRecordID = NewType("TeamRecordID", UUID)


class TeamRecordValue:
    def __init__(self, team_id: TeamID, wins: int, losses: int) -> None:
        self._team_id = team_id
        self._wins = wins
        self._losses = losses

    @property
    def team_id(self) -> TeamID:
        return self._team_id

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


class TeamRecord:
    def __init__(
        self,
        bus: EventBus,
        id_: TeamRecordID,
        season_id: SeasonID,
        week: Optional[int],
        values: list[TeamRecordValue],
    ) -> None:
        self._bus = bus
        self._id = id_
        self._season_id = season_id
        self._week = week
        self._values = values

    @property
    def id_(self) -> TeamRecordID:
        return self._id

    @property
    def season_id(self) -> SeasonID:
        return self._season_id

    @property
    def week(self) -> Optional[int]:
        return self._week

    @property
    def values(self) -> Sequence[TeamRecordValue]:
        return self._values


class TeamRecordFactory:
    def __init__(self, bus: EventBus) -> None:
        self._bus = bus

    def create(
        self,
        season_id: SeasonID,
        week: Optional[int],
        values: list[TeamRecordValue],
    ) -> TeamRecord:
        id_ = TeamRecordID(uuid4())
        record = TeamRecord(self._bus, id_, season_id, week, values)
        self._bus.publish(
            TeamRecordCalculatedEvent(
                event_id=str(uuid4()),
                record_id=str(record.id_),
                season_id=str(record.season_id),
                week=record.week,
                values=[
                    EventValue(
                        team_id=str(value.team_id),
                        wins=value.wins,
                        losses=value.losses,
                        games=value.games,
                        win_percentage=value.win_percentage,
                    )
                    for value in record.values
                ],
            ),
        )

        return record


class TeamRecordRepository(metaclass=ABCMeta):
    @abstractmethod
    def get(self, id_: TeamRecordID) -> Optional[TeamRecord]:
        raise NotImplementedError

    @abstractmethod
    def find(self, season_id: SeasonID, week: Optional[int]) -> Optional[TeamRecord]:
        raise NotImplementedError
