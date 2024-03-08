from uuid import UUID

from fbsrankings.command import CalculateRankingsForSeasonCommand
from fbsrankings.common import EventBus
from fbsrankings.common import QueryBus
from fbsrankings.domain import ColleyMatrixRankingService
from fbsrankings.domain import GameStrengthRankingService
from fbsrankings.domain import SeasonData
from fbsrankings.domain import SimultaneousWinsRankingService
from fbsrankings.domain import SRSRankingService
from fbsrankings.domain import StrengthOfScheduleRankingService
from fbsrankings.domain import TeamRecordService
from fbsrankings.infrastructure import TransactionFactory
from fbsrankings.infrastructure import UnitOfWork
from fbsrankings.query import AffiliationsBySeasonQuery
from fbsrankings.query import GamesBySeasonQuery
from fbsrankings.query import SeasonByIDQuery
from fbsrankings.query import SeasonByYearQuery


class CalculateRankingsForSeasonCommandHandler:
    def __init__(
        self,
        data_source: TransactionFactory,
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

            unit_of_work.commit()
