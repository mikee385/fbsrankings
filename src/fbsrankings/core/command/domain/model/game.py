import datetime
from abc import ABCMeta
from abc import abstractmethod
from typing import NewType
from typing import Optional
from uuid import UUID
from uuid import uuid4

from communication.bus import EventBus
from fbsrankings.core.command.domain.model.season import SeasonID
from fbsrankings.core.command.domain.model.team import TeamID
from fbsrankings.messages.enums import GameStatus
from fbsrankings.messages.enums import SeasonSection
from fbsrankings.messages.event import GameCanceledEvent
from fbsrankings.messages.event import GameCompletedEvent
from fbsrankings.messages.event import GameCreatedEvent
from fbsrankings.messages.event import GameNotesUpdatedEvent
from fbsrankings.messages.event import GameRescheduledEvent


GameID = NewType("GameID", UUID)


class GameStatusError(Exception):
    def __init__(self, message: str, game_id: UUID, status: str) -> None:
        super().__init__(message)
        self.game_id = game_id
        self.status = status


class Game:
    def __init__(
        self,
        bus: EventBus,
        id_: GameID,
        season_id: SeasonID,
        week: int,
        date: datetime.date,
        season_section: SeasonSection,
        home_team_id: TeamID,
        away_team_id: TeamID,
        home_team_score: Optional[int],
        away_team_score: Optional[int],
        status: GameStatus,
        notes: str,
    ) -> None:
        self._bus = bus
        self._id = id_
        self._season_id = season_id
        self._week = week
        self._date = date
        self._season_section = season_section
        self._home_team_id = home_team_id
        self._away_team_id = away_team_id

        self._home_team_score: Optional[int]
        self._away_team_score: Optional[int]
        self._winning_team_id: Optional[TeamID]
        self._winning_team_score: Optional[int]
        self._losing_team_id: Optional[TeamID]
        self._losing_team_score: Optional[int]

        if home_team_score is not None and away_team_score is not None:
            if status != GameStatus.COMPLETED:
                raise ValueError("Game must be COMPLETED in order to have scores")

            self._set_score(home_team_score, away_team_score)

        elif home_team_score is not None:
            raise ValueError("Home team score must be None if away team score is None")

        elif away_team_score is not None:
            raise ValueError("Away team score must be None if home team score is None")

        elif status == GameStatus.COMPLETED:
            raise ValueError("Game must be have scores in order to be COMPLETED")

        else:
            self._home_team_score = None
            self._away_team_score = None
            self._winning_team_id = None
            self._winning_team_score = None
            self._losing_team_id = None
            self._losing_team_score = None

        self._status = status
        self._notes = notes

    @property
    def id_(self) -> GameID:
        return self._id

    @property
    def season_id(self) -> SeasonID:
        return self._season_id

    @property
    def week(self) -> int:
        return self._week

    @property
    def date(self) -> datetime.date:
        return self._date

    @property
    def season_section(self) -> SeasonSection:
        return self._season_section

    @property
    def home_team_id(self) -> TeamID:
        return self._home_team_id

    @property
    def away_team_id(self) -> TeamID:
        return self._away_team_id

    @property
    def home_team_score(self) -> Optional[int]:
        return self._home_team_score

    @property
    def away_team_score(self) -> Optional[int]:
        return self._away_team_score

    @property
    def winning_team_id(self) -> Optional[TeamID]:
        return self._winning_team_id

    @property
    def winning_team_score(self) -> Optional[int]:
        return self._winning_team_score

    @property
    def losing_team_id(self) -> Optional[TeamID]:
        return self._losing_team_id

    @property
    def losing_team_score(self) -> Optional[int]:
        return self._losing_team_score

    @property
    def status(self) -> GameStatus:
        return self._status

    @property
    def notes(self) -> str:
        return self._notes

    def reschedule(self, week: int, date: datetime.date) -> None:
        if self.status != GameStatus.SCHEDULED:
            raise GameStatusError(
                "Game can only be rescheduled if it is still scheduled",
                self.id_,
                self.status.name,
            )

        old_week = self._week
        self._week = week

        old_date = self._date
        self._date = date

        self._bus.publish(
            GameRescheduledEvent(
                str(uuid4()),
                str(self.id_),
                str(self.season_id),
                old_week,
                old_date,
                week,
                date,
                self.season_section.name,
                str(self.home_team_id),
                str(self.away_team_id),
                self.notes,
            ),
        )

    def cancel(self) -> None:
        if self.status != GameStatus.SCHEDULED:
            raise GameStatusError(
                "Game can only be canceled if it is still scheduled",
                self.id_,
                self.status.name,
            )

        self._status = GameStatus.CANCELED

        self._bus.publish(
            GameCanceledEvent(
                str(uuid4()),
                str(self.id_),
                str(self.season_id),
                self.week,
                self.date,
                self.season_section.name,
                str(self.home_team_id),
                str(self.away_team_id),
                self.notes,
            ),
        )

    def complete(self, home_team_score: int, away_team_score: int) -> None:
        if self.status != GameStatus.SCHEDULED:
            raise GameStatusError(
                "Game can only be completed if it is still scheduled",
                self.id_,
                self.status.name,
            )

        if home_team_score is None:
            raise ValueError("Home team score cannot be None")

        if away_team_score is None:
            raise ValueError("Away team score cannot be None")

        self._set_score(home_team_score, away_team_score)

        self._status = GameStatus.COMPLETED

        self._bus.publish(
            GameCompletedEvent(
                str(uuid4()),
                str(self.id_),
                str(self.season_id),
                self.week,
                self.date,
                self.season_section.name,
                str(self.home_team_id),
                str(self.away_team_id),
                home_team_score,
                away_team_score,
                self.notes,
            ),
        )

    def _set_score(self, home_team_score: int, away_team_score: int) -> None:
        self._home_team_score = home_team_score
        self._away_team_score = away_team_score

        if home_team_score > away_team_score:
            self._winning_team_id = self.home_team_id
            self._winning_team_score = self.home_team_score
            self._losing_team_id = self.away_team_id
            self._losing_team_score = self.away_team_score
        elif away_team_score > home_team_score:
            self._winning_team_id = self.away_team_id
            self._winning_team_score = self.away_team_score
            self._losing_team_id = self.home_team_id
            self._losing_team_score = self.home_team_score
        else:
            self._winning_team_id = None
            self._winning_team_score = None
            self._losing_team_id = None
            self._losing_team_score = None

    def update_notes(self, notes: str) -> None:
        old_notes = self._notes
        self._notes = notes

        self._bus.publish(
            GameNotesUpdatedEvent(
                str(uuid4()),
                str(self.id_),
                str(self.season_id),
                self.week,
                self.date,
                self.season_section.name,
                str(self.home_team_id),
                str(self.away_team_id),
                old_notes,
                notes,
            ),
        )


class GameFactory:
    def __init__(self, bus: EventBus) -> None:
        self._bus = bus

    def create(
        self,
        season_id: SeasonID,
        week: int,
        date: datetime.date,
        season_section: SeasonSection,
        home_team_id: TeamID,
        away_team_id: TeamID,
        notes: str,
    ) -> Game:
        id_ = GameID(uuid4())
        game = Game(
            self._bus,
            id_,
            season_id,
            week,
            date,
            season_section,
            home_team_id,
            away_team_id,
            None,
            None,
            GameStatus.SCHEDULED,
            notes,
        )
        self._bus.publish(
            GameCreatedEvent(
                str(uuid4()),
                str(game.id_),
                str(game.season_id),
                game.week,
                game.date,
                game.season_section.name,
                str(game.home_team_id),
                str(game.away_team_id),
                game.notes,
            ),
        )

        return game


class GameRepository(metaclass=ABCMeta):
    @abstractmethod
    def get(self, id_: GameID) -> Optional[Game]:
        raise NotImplementedError

    @abstractmethod
    def find(
        self,
        season_id: SeasonID,
        week: int,
        team1_id: TeamID,
        team2_id: TeamID,
    ) -> Optional[Game]:
        raise NotImplementedError
