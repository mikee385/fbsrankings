from pathlib import Path
from typing import Any

from fbsrankings.cli.main import main

from .copy_files import _copy_files


def test_main_seasons_full(
    capsys: Any,
    output_path: Path,
    data_path: Path,
    test_path: Path,
    query_config: Path,
) -> None:
    _copy_files(data_path, test_path, ["test_data.db", "test_data.json"])
    files = _copy_files(output_path, test_path, ["main_seasons_full.txt"])
    with files[0].open(mode="r", encoding="utf-8") as expected_file:
        expected_out = expected_file.read()

    exit_result = main(["seasons", f"--config={query_config}"])
    assert exit_result == 0

    captured_out, captured_err = capsys.readouterr()
    assert captured_out == expected_out
    assert captured_err == ""


def test_main_seasons_empty(
    capsys: Any,
    output_path: Path,
    data_path: Path,
    test_path: Path,
    command_config: Path,
) -> None:
    _copy_files(data_path, test_path, ["empty_data.db", "empty_data.json"])
    files = _copy_files(output_path, test_path, ["main_seasons_empty.txt"])
    with files[0].open(mode="r", encoding="utf-8") as expected_file:
        expected_err = expected_file.read()

    exit_result = main(["seasons", f"--config={command_config}"])
    assert exit_result == 1

    captured_out, captured_err = capsys.readouterr()
    assert captured_out == ""
    assert captured_err == expected_err
