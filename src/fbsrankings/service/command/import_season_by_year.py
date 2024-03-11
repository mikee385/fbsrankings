from fbsrankings.command import ImportSeasonByYearCommand
from fbsrankings.common import EventBus
from fbsrankings.domain import ImportService
from fbsrankings.domain import ValidationService
from fbsrankings.infrastructure import DataSource
from fbsrankings.infrastructure import UnitOfWork
from fbsrankings.infrastructure.sportsreference import SportsReference
from fbsrankings.service.config import Config


class ImportSeasonByYearCommandHandler:
    def __init__(
        self,
        config: Config,
        data_source: DataSource,
        event_bus: EventBus,
        validation_service: ValidationService,
    ) -> None:
        self._config = config
        self._data_source = data_source
        self._event_bus = event_bus
        self._validation_service = validation_service

    def __call__(self, command: ImportSeasonByYearCommand) -> None:
        alternate_names = self._config.alternate_names
        if alternate_names is None:
            alternate_names = {}

        with UnitOfWork(self._data_source, self._event_bus) as unit_of_work:
            import_service = ImportService(unit_of_work)
            sports_reference = SportsReference(
                alternate_names,
                import_service,
                self._validation_service,
            )
            sports_reference.import_season(command.year)
            try:
                unit_of_work.commit()
            except Exception:
                unit_of_work.rollback()
                raise
