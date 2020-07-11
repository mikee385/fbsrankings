from typing import Any
from typing import List
from typing import Optional
from uuid import UUID

from fbsrankings.common import Event
from fbsrankings.common import EventBus
from fbsrankings.common import Identifier
from fbsrankings.domain import GameID
from fbsrankings.domain import Ranking
from fbsrankings.domain import RankingID
from fbsrankings.domain import RankingRepository as BaseRepository
from fbsrankings.domain import RankingType
from fbsrankings.domain import RankingValue
from fbsrankings.domain import SeasonID
from fbsrankings.domain import TeamID
from fbsrankings.event import RankingCalculatedEvent
from fbsrankings.infrastructure.memory.storage import RankingDto
from fbsrankings.infrastructure.memory.storage import RankingStorage
from fbsrankings.infrastructure.memory.storage import RankingValueDto


class RankingRepository(BaseRepository):
    def __init__(self, storage: RankingStorage, bus: EventBus) -> None:
        super().__init__(bus)
        self._storage = storage

    def get(self, ID: RankingID) -> Optional[Ranking[Any]]:
        dto = self._storage.get(ID.value)
        return self._to_ranking(dto) if dto is not None else None

    def find(
        self, name: str, season_ID: SeasonID, week: Optional[int],
    ) -> Optional[Ranking[Any]]:
        dto = self._storage.find(name, season_ID.value, week)
        return self._to_ranking(dto) if dto is not None else None

    def for_season(self, season_ID: SeasonID) -> List[Ranking[Any]]:
        dtos = self._storage.for_season(season_ID.value)
        return [self._to_ranking(dto) for dto in dtos if dto is not None]

    def _to_ranking(self, dto: RankingDto) -> Ranking[Any]:
        return Ranking[Any](
            self._bus,
            RankingID(dto.ID),
            dto.name,
            RankingType[dto.type],
            SeasonID(dto.season_ID),
            dto.week,
            [RankingValue(self._value_id(value.ID), value.order, value.rank, value.value) for value in dto.values]
        )

    def handle(self, event: Event) -> bool:
        if isinstance(event, RankingCalculatedEvent):
            self._handle_ranking_calculated(event)
            return True
        else:
            return False

    def _handle_ranking_calculated(self, event: RankingCalculatedEvent) -> None:
        self._storage.add(
            RankingDto(
                event.ID,
                event.name,
                event.type,
                event.season_ID,
                event.week,
                [RankingValueDto(value.ID, value.order, value.rank, value.value) for value in event.values],
            )
        )
        
    def _value_ID(self, type: str, ID: UUID) -> Identifier:
        if type == RankingType.TEAM.name:
            return TeamID(ID)
        elif type == RankingType.GAME.name:
            return GameID(ID)
        else:
            raise ValueError(f"Unknown ranking type: {type}")

