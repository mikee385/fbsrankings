import sys
import threading
import time
from collections.abc import Iterable
from collections.abc import Iterator
from collections.abc import Sized
from types import TracebackType
from typing import ContextManager
from typing import Generic
from typing import Literal
from typing import Optional
from typing import Protocol
from typing import TypeVar


T = TypeVar("T", covariant=True)


class Progressable(Iterable[T], Sized, Generic[T], Protocol):
    pass


class ProgressBar(Generic[T]):
    def __init__(
        self,
        iterable: Progressable[T],
        length: int = 40,
        fill: str = "█",
    ) -> None:
        self._iterable = iterable
        self._total = len(iterable)
        self._length = length
        self._fill = fill

        self._start_time: float
        self._current: int
        self._iterator: Iterator[T]

    def __iter__(self) -> Iterator[T]:
        self._start_time = time.time()
        self._current = 0
        self._iterator = self._iterable.__iter__()
        return self

    def __next__(self) -> T:
        if self._current == self._total:
            self._print_complete()
            raise StopIteration
        self._print_progress(self._current)
        self._current += 1
        return self._iterator.__next__()

    def _print_progress(self, iteration: int) -> None:
        percent = iteration / self._total
        filled_length = int(self._length * percent)
        progress_bar = self._fill * filled_length + "-" * (self._length - filled_length)

        sys.stderr.write(
            f"\r{percent * 100:>5.1f}% |{progress_bar}| {iteration}/{self._total}",
        )

        if iteration > 0:
            elapsed_time = time.time() - self._start_time
            time_per_iteration = elapsed_time / iteration if iteration > 0 else 0
            remaining_time = time_per_iteration * (self._total - iteration)

            sys.stderr.write(
                f" [{format_time(elapsed_time)}<{format_time(remaining_time)},"
                f" {format_time(time_per_iteration)}s/it]",
            )

        sys.stderr.flush()

    def _print_complete(self) -> None:
        self._print_progress(self._total)
        sys.stderr.write("\n")
        sys.stderr.flush()


class Spinner(ContextManager["Spinner"]):
    def __init__(self) -> None:
        self._sequence = ["|", "/", "-", "\\"]

        self._start_time: float
        self._counter: int
        self._busy: bool
        self._thread: threading.Thread

    def _spinner_task(self) -> None:
        while self._busy:
            sys.stderr.write(
                f"\r{self._sequence[self._counter % len(self._sequence)]} Processing...",
            )
            sys.stderr.flush()
            time.sleep(0.1)
            self._counter += 1

    def __enter__(self) -> "Spinner":
        self._start_time = time.time()
        self._counter = 0
        self._busy = True

        self._thread = threading.Thread(target=self._spinner_task)
        self._thread.start()

        return self

    def __exit__(
        self,
        type_: Optional[type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        elapsed_time = time.time() - self._start_time
        self._busy = False
        self._thread.join()

        sys.stderr.write(f"\rDone! [{format_time(elapsed_time)}]  \n")

        return False


def format_time(timestamp: float) -> str:
    return time.strftime("%M:%S", time.gmtime(timestamp))
