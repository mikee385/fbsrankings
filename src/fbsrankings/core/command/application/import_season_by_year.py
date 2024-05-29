from fbsrankings.core.command.domain.service.importer import Importer
from fbsrankings.core.command.domain.service.validator import Validator
from fbsrankings.core.command.infrastructure.data_source import DataSource
from fbsrankings.core.command.infrastructure.sports_reference import SportsReference
from fbsrankings.core.command.infrastructure.transaction.transaction import Transaction
from fbsrankings.shared.command import ImportSeasonByYearCommand
from fbsrankings.shared.config import Config
from fbsrankings.shared.messaging import EventBus


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

        validator = Validator(self._event_bus)

        with Transaction(self._data_source, self._event_bus) as transaction:
            importer = Importer(transaction.factory, transaction.repository)
            sports_reference = SportsReference(
                alternate_names,
                importer,
                validator,
            )
            sports_reference.import_season(command.year)
            try:
                transaction.commit()
            except Exception:
                transaction.rollback()
                raise
