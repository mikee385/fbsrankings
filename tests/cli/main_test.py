# pylint: disable=redefined-outer-name
from pathlib import Path
from typing import Any

from fbsrankings import __version__
from fbsrankings.cli.main import main

from .copy_files import _copy_files


def test_main_help(
    capsys: Any,
    output_path: Path,
    test_path: Path,
    option_config: Path,
) -> None:
    files = _copy_files(output_path, test_path, ["main_help.txt"])
    with files[0].open(mode="r", encoding="utf-8") as expected_file:
        expected_out = expected_file.read()

    exit_result = main(["--help", f"--config={option_config}"])
    assert exit_result == 0

    captured_out, captured_err = capsys.readouterr()
    assert captured_out == expected_out
    assert captured_err == ""


def test_main_version(capsys: Any, option_config: Path) -> None:
    exit_result = main(["--version", f"--config={option_config}"])
    assert exit_result == 0

    captured_out, captured_err = capsys.readouterr()
    assert captured_out == f"{__version__}\n"
    assert captured_err == ""


def test_main_missing_command(
    capsys: Any,
    output_path: Path,
    test_path: Path,
    option_config: Path,
) -> None:
    files = _copy_files(output_path, test_path, ["main_missing_command.txt"])
    with files[0].open(mode="r", encoding="utf-8") as expected_file:
        expected_out = expected_file.read()

    exit_result = main([f"--config={option_config}"])
    assert exit_result == 0

    captured_out, captured_err = capsys.readouterr()
    assert captured_out == expected_out
    assert captured_err == ""


def test_main_invalid_command(
    capsys: Any,
    output_path: Path,
    test_path: Path,
    option_config: Path,
) -> None:
    files = _copy_files(output_path, test_path, ["main_invalid_command.txt"])
    with files[0].open(mode="r", encoding="utf-8") as expected_file:
        expected_err = expected_file.read()

    exit_result = main(["invalid", f"--config={option_config}"])
    assert exit_result == 2

    captured_out, captured_err = capsys.readouterr()
    assert captured_out == ""
    assert expected_err == captured_err
