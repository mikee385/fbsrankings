import threading
import time
from types import TracebackType
from typing import Optional
from typing import Type

from tqdm import tqdm
from typing_extensions import Literal


class Spinner:
    def __init__(self, delay: Optional[float] = None) -> None:
        self.busy = False
        self.total = 0
        self.increment = 1

        if delay and float(delay):
            self.delay = delay
        else:
            self.delay = 0.01

    def _spinner_task(self) -> None:
        while self.busy:
            time.sleep(self.delay)

            self.bar.update(self.increment)
            self.bar.refresh()

            self.total += self.increment
            if self.total == 0:
                self.increment = 1
            elif self.total == 100:
                self.increment = -1

    def __enter__(self) -> "Spinner":
        self.bar = tqdm(total=100, bar_format="{desc}|{bar:10}| {elapsed}")
        self.bar.set_description_str("    ")

        self.busy = True
        self.total = 0
        self.increment = 1

        threading.Thread(target=self._spinner_task).start()

        return self

    def __exit__(
        self,
        type: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.busy = False
        time.sleep(self.delay)

        self.bar.set_description_str("100%")
        if self.total == 0:
            self.bar.update(99)
            self.bar.refresh()
        elif self.total < 100:
            self.bar.update(100 - self.total)
            self.bar.refresh()

        self.bar.close()

        return False
