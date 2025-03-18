from pathlib import Path
from typing import Any

from fbsrankings.cli.main import main

from .copy_files import _copy_files


def test_main_games_full(
    capsys: Any,
    output_path: Path,
    data_path: Path,
    test_path: Path,
    query_config: Path,
) -> None:
    _copy_files(data_path, test_path, ["test_data.db", "test_data.json"])
    files = _copy_files(output_path, test_path, ["main_games_full.txt"])
    with files[0].open(mode="r", encoding="utf-8") as expected_file:
        expected_out = expected_file.read()

    exit_result = main(["games", f"--config={query_config}"])
    assert exit_result == 0

    captured_out, captured_err = capsys.readouterr()
    assert captured_out == expected_out
    assert captured_err == ""


def test_main_games_empty(
    capsys: Any,
    output_path: Path,
    data_path: Path,
    test_path: Path,
    command_config: Path,
) -> None:
    _copy_files(data_path, test_path, ["empty_data.db", "empty_data.json"])
    files = _copy_files(output_path, test_path, ["main_games_empty.txt"])
    with files[0].open(mode="r", encoding="utf-8") as expected_file:
        expected_out = expected_file.read()

    exit_result = main(["games", f"--config={command_config}"])
    assert exit_result == 0

    captured_out, captured_err = capsys.readouterr()
    assert captured_out == expected_out
    assert captured_err == ""


def test_main_games_year_full(
    capsys: Any,
    output_path: Path,
    data_path: Path,
    test_path: Path,
    query_config: Path,
) -> None:
    _copy_files(data_path, test_path, ["test_data.db", "test_data.json"])
    files = _copy_files(output_path, test_path, ["main_games_2012_full.txt"])
    with files[0].open(mode="r", encoding="utf-8") as expected_file:
        expected_out = expected_file.read()

    exit_result = main(["games", "2012", f"--config={query_config}"])
    assert exit_result == 0

    captured_out, captured_err = capsys.readouterr()
    assert captured_out == expected_out
    assert captured_err == ""


def test_main_games_year_empty(
    capsys: Any,
    output_path: Path,
    data_path: Path,
    test_path: Path,
    command_config: Path,
) -> None:
    _copy_files(data_path, test_path, ["empty_data.db", "empty_data.json"])
    files = _copy_files(output_path, test_path, ["main_games_2012_empty.txt"])
    with files[0].open(mode="r", encoding="utf-8") as expected_file:
        expected_out = expected_file.read()

    exit_result = main(["games", "2012", f"--config={command_config}"])
    assert exit_result == 0

    captured_out, captured_err = capsys.readouterr()
    assert captured_out == expected_out
    assert captured_err == ""


def test_main_games_week_full(
    capsys: Any,
    output_path: Path,
    data_path: Path,
    test_path: Path,
    query_config: Path,
) -> None:
    _copy_files(data_path, test_path, ["test_data.db", "test_data.json"])
    files = _copy_files(output_path, test_path, ["main_games_2012w9_full.txt"])
    with files[0].open(mode="r", encoding="utf-8") as expected_file:
        expected_out = expected_file.read()

    exit_result = main(["games", "2012w9", f"--config={query_config}"])
    assert exit_result == 0

    captured_out, captured_err = capsys.readouterr()
    assert captured_out == expected_out
    assert captured_err == ""


def test_main_games_week_empty(
    capsys: Any,
    output_path: Path,
    data_path: Path,
    test_path: Path,
    command_config: Path,
) -> None:
    _copy_files(data_path, test_path, ["empty_data.db", "empty_data.json"])
    files = _copy_files(output_path, test_path, ["main_games_2012w9_empty.txt"])
    with files[0].open(mode="r", encoding="utf-8") as expected_file:
        expected_out = expected_file.read()

    exit_result = main(["games", "2012w9", f"--config={command_config}"])
    assert exit_result == 0

    captured_out, captured_err = capsys.readouterr()
    assert captured_out == expected_out
    assert captured_err == ""
