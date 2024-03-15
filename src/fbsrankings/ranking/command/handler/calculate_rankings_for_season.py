from uuid import UUID

from fbsrankings.common import EventBus
from fbsrankings.common import QueryBus
from fbsrankings.core.query import AffiliationsBySeasonQuery
from fbsrankings.core.query import GamesBySeasonQuery
from fbsrankings.core.query import SeasonByIDQuery
from fbsrankings.core.query import SeasonByYearQuery
from fbsrankings.ranking.command.command.calculate_rankings_for_season import (
    CalculateRankingsForSeasonCommand,
)
from fbsrankings.ranking.command.domain.model.ranking import SeasonData
from fbsrankings.ranking.command.domain.service.colley_matrix_ranking_service import (
    ColleyMatrixRankingService,
)
from fbsrankings.ranking.command.domain.service.game_strength_ranking_service import (
    GameStrengthRankingService,
)
from fbsrankings.ranking.command.domain.service.record_service import TeamRecordService
from fbsrankings.ranking.command.domain.service.simultaneous_wins_ranking_service import (
    SimultaneousWinsRankingService,
)
from fbsrankings.ranking.command.domain.service.srs_ranking_service import (
    SRSRankingService,
)
from fbsrankings.ranking.command.domain.service.strength_of_schedule_ranking_service import (
    StrengthOfScheduleRankingService,
)
from fbsrankings.ranking.command.infrastructure.data_source import DataSource
from fbsrankings.ranking.command.infrastructure.unit_of_work.unit_of_work import (
    UnitOfWork,
)


class CalculateRankingsForSeasonCommandHandler:
    def __init__(
        self,
        data_source: DataSource,
        query_bus: QueryBus,
        event_bus: EventBus,
    ) -> None:
        self._data_source = data_source
        self._query_bus = query_bus
        self._event_bus = event_bus

    def __call__(self, command: CalculateRankingsForSeasonCommand) -> None:
        with UnitOfWork(self._data_source, self._event_bus) as unit_of_work:
            if isinstance(command.season_id_or_year, UUID):
                season_by_id = self._query_bus.query(
                    SeasonByIDQuery(command.season_id_or_year),
                )
                if season_by_id is None:
                    raise ValueError(
                        f"Season not found for {command.season_id_or_year}",
                    )
                season_id = season_by_id.id_

            elif isinstance(command.season_id_or_year, int):
                season_by_year = self._query_bus.query(
                    SeasonByYearQuery(command.season_id_or_year),
                )
                if season_by_year is None:
                    raise ValueError(
                        f"Season not found for {command.season_id_or_year}",
                    )
                season_id = season_by_year.id_

            else:
                raise TypeError("season_id_or_year must be of type UUID or int")

            affiliations = self._query_bus.query(
                AffiliationsBySeasonQuery(season_id),
            ).affiliations
            games = self._query_bus.query(GamesBySeasonQuery(season_id)).games

            season_data = SeasonData(season_id, affiliations, games)

            TeamRecordService(unit_of_work.team_record).calculate_for_season(
                season_data,
            )

            srs_rankings = SRSRankingService(
                unit_of_work.team_ranking,
            ).calculate_for_season(season_data)
            for ranking in srs_rankings:
                StrengthOfScheduleRankingService(
                    unit_of_work.team_ranking,
                ).calculate_for_ranking(season_data, ranking)
                GameStrengthRankingService(
                    unit_of_work.game_ranking,
                ).calculate_for_ranking(season_data, ranking)

            cm_rankings = ColleyMatrixRankingService(
                unit_of_work.team_ranking,
            ).calculate_for_season(season_data)
            for ranking in cm_rankings:
                StrengthOfScheduleRankingService(
                    unit_of_work.team_ranking,
                ).calculate_for_ranking(season_data, ranking)
                GameStrengthRankingService(
                    unit_of_work.game_ranking,
                ).calculate_for_ranking(season_data, ranking)

            sw_rankings = SimultaneousWinsRankingService(
                unit_of_work.team_ranking,
            ).calculate_for_season(season_data)
            for ranking in sw_rankings:
                StrengthOfScheduleRankingService(
                    unit_of_work.team_ranking,
                ).calculate_for_ranking(season_data, ranking)
                GameStrengthRankingService(
                    unit_of_work.game_ranking,
                ).calculate_for_ranking(season_data, ranking)

            try:
                unit_of_work.commit()
            except Exception:
                unit_of_work.rollback()
                raise
