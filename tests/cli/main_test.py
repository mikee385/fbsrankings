from typing import Any

import pytest

from fbsrankings import __version__
from fbsrankings.cli import main


def test_main_help(capsys: Any) -> None:
    with pytest.raises(SystemExit) as exit_result:
        main(["--help"])
    assert exit_result.type == SystemExit
    assert exit_result.value.code == 0

    captured = capsys.readouterr()
    assert len(captured.out) > 0
    assert len(captured.err) == 0


def test_main_version(capsys: Any) -> None:
    with pytest.raises(SystemExit) as exit_result:
        main(["--version"])
    assert exit_result.type == SystemExit
    assert exit_result.value.code == 0

    captured = capsys.readouterr()
    assert captured.out == f"{__version__}\n"
    assert len(captured.err) == 0


def test_main_missing_command(capsys: Any) -> None:
    with pytest.raises(SystemExit) as exit_result:
        main([])
    assert exit_result.type == SystemExit
    assert exit_result.value.code == 0

    captured = capsys.readouterr()
    assert len(captured.out) > 0
    assert len(captured.err) == 0


def test_main_invalid_command(capsys: Any) -> None:
    with pytest.raises(SystemExit) as exit_result:
        main(["invalid"])
    assert exit_result.type == SystemExit
    assert exit_result.value.code == 2

    captured = capsys.readouterr()
    assert len(captured.out) == 0
    assert len(captured.err) > 0
