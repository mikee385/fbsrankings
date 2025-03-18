from pathlib import Path
from typing import Any

from fbsrankings.cli.main import main

from .copy_files import _copy_files


def test_main_teams(
    capsys: Any,
    output_path: Path,
    data_path: Path,
    test_path: Path,
    query_config: Path,
) -> None:
    _copy_files(data_path, test_path, ["test_data.db", "test_data.json"])
    files = _copy_files(output_path, test_path, ["main_teams.txt"])
    with files[0].open(mode="r", encoding="utf-8") as expected_file:
        expected_out = expected_file.read()

    exit_result = main(["teams", f"--config={query_config}"])
    assert exit_result == 0

    captured_out, captured_err = capsys.readouterr()
    assert captured_out == expected_out
    assert captured_err == ""


def test_main_teams_year(
    capsys: Any,
    output_path: Path,
    data_path: Path,
    test_path: Path,
    query_config: Path,
) -> None:
    _copy_files(data_path, test_path, ["test_data.db", "test_data.json"])
    files = _copy_files(output_path, test_path, ["main_teams_2012.txt"])
    with files[0].open(mode="r", encoding="utf-8") as expected_file:
        expected_out = expected_file.read()

    exit_result = main(["teams", "2012", f"--config={query_config}"])
    assert exit_result == 0

    captured_out, captured_err = capsys.readouterr()
    assert captured_out == expected_out
    assert captured_err == ""


def test_main_teams_week(
    capsys: Any,
    output_path: Path,
    data_path: Path,
    test_path: Path,
    query_config: Path,
) -> None:
    _copy_files(data_path, test_path, ["test_data.db", "test_data.json"])
    files = _copy_files(output_path, test_path, ["main_teams_2012w9.txt"])
    with files[0].open(mode="r", encoding="utf-8") as expected_file:
        expected_out = expected_file.read()

    exit_result = main(["teams", "2012w9", f"--config={query_config}"])
    assert exit_result == 0

    captured_out, captured_err = capsys.readouterr()
    assert captured_out == expected_out
    assert captured_err == ""
