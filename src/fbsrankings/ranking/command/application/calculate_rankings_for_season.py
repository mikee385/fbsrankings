from uuid import UUID
from uuid import uuid4

from communication.bus import EventBus
from communication.bus import QueryBus
from fbsrankings.messages.command import CalculateRankingsForSeasonCommand
from fbsrankings.messages.query import AffiliationsBySeasonQuery
from fbsrankings.messages.query import AffiliationsBySeasonResult
from fbsrankings.messages.query import GamesBySeasonQuery
from fbsrankings.messages.query import GamesBySeasonResult
from fbsrankings.messages.query import SeasonByIDQuery
from fbsrankings.messages.query import SeasonByIDResult
from fbsrankings.messages.query import SeasonByYearQuery
from fbsrankings.messages.query import SeasonByYearResult
from fbsrankings.ranking.command.domain.model.ranking import SeasonData
from fbsrankings.ranking.command.domain.service.colley_matrix_ranking_calculator import (
    ColleyMatrixRankingCalculator,
)
from fbsrankings.ranking.command.domain.service.game_strength_ranking_calculator import (
    GameStrengthRankingCalculator,
)
from fbsrankings.ranking.command.domain.service.record_calculator import (
    TeamRecordCalculator,
)
from fbsrankings.ranking.command.domain.service.simultaneous_wins_ranking_calculator import (
    SimultaneousWinsRankingCalculator,
)
from fbsrankings.ranking.command.domain.service.srs_ranking_calculator import (
    SRSRankingCalculator,
)
from fbsrankings.ranking.command.domain.service.strength_of_schedule_ranking_calculator import (
    StrengthOfScheduleRankingCalculator,
)
from fbsrankings.ranking.command.infrastructure.data_source import DataSource
from fbsrankings.ranking.command.infrastructure.transaction.transaction import (
    Transaction,
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
        with Transaction(self._data_source, self._event_bus) as transaction:
            season_id_or_year = command.WhichOneof("season_id_or_year")
            if season_id_or_year == "season_id":
                season_by_id = self._query_bus.query(
                    SeasonByIDQuery(query_id=str(uuid4()), season_id=command.season_id),
                    SeasonByIDResult,
                )
                if season_by_id is None:
                    raise ValueError(
                        f"Season not found for {command.season_id}",
                    )
                season_id = season_by_id.season_id

            elif season_id_or_year == "year":
                season_by_year = self._query_bus.query(
                    SeasonByYearQuery(query_id=str(uuid4()), year=command.year),
                    SeasonByYearResult,
                )
                if season_by_year is None:
                    raise ValueError(
                        f"Season not found for {command.year}",
                    )
                season_id = season_by_year.season_id

            else:
                raise TypeError("season_id_or_year must be of type str or int")

            affiliations = self._query_bus.query(
                AffiliationsBySeasonQuery(
                    query_id=str(uuid4()),
                    season_id=season_id,
                ),
                AffiliationsBySeasonResult,
            ).affiliations
            games = self._query_bus.query(
                GamesBySeasonQuery(query_id=str(uuid4()), season_id=season_id),
                GamesBySeasonResult,
            ).games

            season_data = SeasonData(UUID(season_id), affiliations, games)

            TeamRecordCalculator(transaction.factory.team_record).calculate_for_season(
                season_data,
            )

            srs_rankings = SRSRankingCalculator(
                transaction.factory.team_ranking,
            ).calculate_for_season(season_data)
            for ranking in srs_rankings:
                StrengthOfScheduleRankingCalculator(
                    transaction.factory.team_ranking,
                ).calculate_for_ranking(season_data, ranking)
                GameStrengthRankingCalculator(
                    transaction.factory.game_ranking,
                ).calculate_for_ranking(season_data, ranking)

            cm_rankings = ColleyMatrixRankingCalculator(
                transaction.factory.team_ranking,
            ).calculate_for_season(season_data)
            for ranking in cm_rankings:
                StrengthOfScheduleRankingCalculator(
                    transaction.factory.team_ranking,
                ).calculate_for_ranking(season_data, ranking)
                GameStrengthRankingCalculator(
                    transaction.factory.game_ranking,
                ).calculate_for_ranking(season_data, ranking)

            sw_rankings = SimultaneousWinsRankingCalculator(
                transaction.factory.team_ranking,
            ).calculate_for_season(season_data)
            for ranking in sw_rankings:
                StrengthOfScheduleRankingCalculator(
                    transaction.factory.team_ranking,
                ).calculate_for_ranking(season_data, ranking)
                GameStrengthRankingCalculator(
                    transaction.factory.game_ranking,
                ).calculate_for_ranking(season_data, ranking)

            try:
                transaction.commit()
            except Exception:
                transaction.rollback()
                raise
