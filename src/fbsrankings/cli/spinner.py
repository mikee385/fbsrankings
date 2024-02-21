import threading
import time
from types import TracebackType
from typing import Optional
from typing import Type

from tqdm import tqdm
from typing_extensions import Literal


class Spinner:
    def __init__(self, delay: Optional[float] = None) -> None:
        self._bar = tqdm(
            total=100, bar_format="{desc}|{bar:10}| {elapsed}",  # noqa: FS003
        )

        self._busy = False
        self._total = 0
        self._increment = 1

        if delay and float(delay):
            self._delay = delay
        else:
            self._delay = 0.01

    def _spinner_task(self) -> None:
        while self._busy:
            time.sleep(self._delay)

            self._bar.update(self._increment)
            self._bar.refresh()

            self._total += self._increment
            if self._total == 0:
                self._increment = 1
            elif self._total == 100:
                self._increment = -1

    def __enter__(self) -> "Spinner":
        self._bar.set_description_str("    ")

        self._busy = True
        self._total = 0
        self._increment = 1

        threading.Thread(target=self._spinner_task).start()

        return self

    def __exit__(
        self,
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self._busy = False
        time.sleep(self._delay)

        self._bar.set_description_str("100%")
        if self._total == 0:
            self._bar.update(99)
            self._bar.refresh()
        elif self._total < 100:
            self._bar.update(100 - self._total)
            self._bar.refresh()

        self._bar.close()

        return False
