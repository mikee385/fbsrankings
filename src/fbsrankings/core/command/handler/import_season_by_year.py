from fbsrankings.common import EventBus
from fbsrankings.config import Config
from fbsrankings.core.command.command.import_season_by_year import (
    ImportSeasonByYearCommand,
)
from fbsrankings.core.command.domain.service.import_service import ImportService
from fbsrankings.core.command.domain.service.validation_service import ValidationService
from fbsrankings.core.command.infrastructure.data_source import DataSource
from fbsrankings.core.command.infrastructure.sports_reference import SportsReference
from fbsrankings.core.command.infrastructure.unit_of_work.unit_of_work import UnitOfWork


class ImportSeasonByYearCommandHandler:
    def __init__(
        self,
        config: Config,
        data_source: DataSource,
        event_bus: EventBus,
    ) -> None:
        self._config = config
        self._data_source = data_source
        self._event_bus = event_bus

    def __call__(self, command: ImportSeasonByYearCommand) -> None:
        alternate_names = self._config.alternate_names
        if alternate_names is None:
            alternate_names = {}

        validation_service = ValidationService(self._event_bus)

        with UnitOfWork(self._data_source, self._event_bus) as unit_of_work:
            import_service = ImportService(unit_of_work)
            sports_reference = SportsReference(
                alternate_names,
                import_service,
                validation_service,
            )
            sports_reference.import_season(command.year)
            try:
                unit_of_work.commit()
            except Exception:
                unit_of_work.rollback()
                raise
