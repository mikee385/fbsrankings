# pylint: disable=redefined-outer-name
import shutil
import sys
from collections.abc import Sequence
from configparser import ConfigParser
from pathlib import Path
from typing import Any

import pytest

from fbsrankings import __version__
from fbsrankings.cli.main import main


def _copy_files(src_dir: Path, dest_dir: Path, files: Sequence[str]) -> Sequence[Path]:
    file_paths: list[Path] = []

    for file in files:
        src_path = src_dir / file
        dest_path = dest_dir / file

        max_version = (3, 12)
        min_version = (3, 6)
        if sys.version_info > max_version:
            current_version = max_version
        elif sys.version_info < min_version:
            current_version = min_version
        else:
            current_version = (sys.version_info.major, sys.version_info.minor)

        for minor in range(current_version[1], min_version[1] - 1, -1):
            version_path = src_dir / f"Python{current_version[0]}{minor}" / file
            if version_path.exists():
                src_path = version_path
                break

        shutil.copyfile(src_path, dest_path)
        file_paths.append(dest_path)

    return file_paths


def _build_config_file(config_path: Path, config_file: str, test_path: Path) -> Path:
    common_path = config_path / "common.ini"
    src_path = config_path / config_file
    dest_path = test_path / "test_config.ini"
    sqlite_path = test_path / "test_data.db"
    tinydb_path = test_path / "test_data.json"

    parser = ConfigParser()
    parser.read(common_path)
    parser.read(src_path)
    if parser["fbsrankings"]["storage"] in ("sqlite-shared", "sqlite-tinydb"):
        parser.add_section("fbsrankings.sqlite")
        parser.set("fbsrankings.sqlite", "file", str(sqlite_path))
    if parser["fbsrankings"]["storage"] == "sqlite-tinydb":
        parser.add_section("fbsrankings.tinydb")
        parser.set("fbsrankings.tinydb", "file", str(tinydb_path))
    with dest_path.open(mode="w", encoding="utf-8") as dest_file:
        parser.write(dest_file)

    return dest_path


@pytest.fixture()
def config_path(request: Any) -> Path:
    filename = request.module.__file__
    test_dir = Path(filename).parent.parent
    return test_dir / "config"


@pytest.fixture()
def data_path(request: Any) -> Path:
    filename = request.module.__file__
    test_dir = Path(filename).parent.parent
    return test_dir / "data"


@pytest.fixture()
def output_path(request: Any) -> Path:
    filename = request.module.__file__
    test_dir = Path(filename).parent.parent
    return test_dir / "output"


@pytest.fixture()
def test_path(tmpdir: Any) -> Path:
    return Path(str(tmpdir))


@pytest.fixture(params=["memory.ini"])
def option_config(request: Any, config_path: Path, test_path: Path) -> Path:
    return _build_config_file(config_path, request.param, test_path)


@pytest.fixture(params=["memory.ini", "sqlite.ini", "tinydb.ini"])
def command_config(request: Any, config_path: Path, test_path: Path) -> Path:
    return _build_config_file(config_path, request.param, test_path)


@pytest.fixture(params=["sqlite.ini", "tinydb.ini"])
def query_config(request: Any, config_path: Path, test_path: Path) -> Path:
    return _build_config_file(config_path, request.param, test_path)


@pytest.fixture()
def test_seasons() -> list[str]:
    return ["2012", "2013"]


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


def test_main_import(
    capsys: Any,
    output_path: Path,
    test_path: Path,
    command_config: Path,
    test_seasons: list[str],
) -> None:
    files = _copy_files(
        output_path,
        test_path,
        ["main_import_2012_2013_drop_check.txt"],
    )
    with files[0].open(mode="r", encoding="utf-8") as expected_file:
        expected_out = expected_file.read()

    exit_result = main(
        [
            "import",
            *test_seasons,
            "--drop",
            "--check",
            f"--config={command_config}",
            "--trace",
        ],
    )
    assert exit_result == 0

    captured_out, captured_err = capsys.readouterr()
    assert captured_out == expected_out
    assert "Dropping existing data:" in captured_err
    assert "Importing season data:" in captured_err
    assert "Calculating rankings:" in captured_err


def test_main_seasons(
    capsys: Any,
    output_path: Path,
    data_path: Path,
    test_path: Path,
    query_config: Path,
) -> None:
    _copy_files(data_path, test_path, ["test_data.db", "test_data.json"])
    files = _copy_files(output_path, test_path, ["main_seasons.txt"])
    with files[0].open(mode="r", encoding="utf-8") as expected_file:
        expected_out = expected_file.read()

    exit_result = main(["seasons", f"--config={query_config}"])
    assert exit_result == 0

    captured_out, captured_err = capsys.readouterr()
    assert captured_out == expected_out
    assert captured_err == ""


def test_main_latest(
    capsys: Any,
    output_path: Path,
    data_path: Path,
    test_path: Path,
    query_config: Path,
) -> None:
    _copy_files(data_path, test_path, ["test_data.db", "test_data.json"])
    files = _copy_files(output_path, test_path, ["main_latest.txt"])
    with files[0].open(mode="r", encoding="utf-8") as expected_file:
        expected_out = expected_file.read()

    exit_result = main(["latest", f"--config={query_config}"])
    assert exit_result == 0

    captured_out, captured_err = capsys.readouterr()
    assert captured_out == expected_out
    assert captured_err == ""


def test_main_latest_rating_srs_top_5(
    capsys: Any,
    output_path: Path,
    data_path: Path,
    test_path: Path,
    query_config: Path,
) -> None:
    _copy_files(data_path, test_path, ["test_data.db", "test_data.json"])
    files = _copy_files(
        output_path,
        test_path,
        ["main_latest_rating_colley_matrix_top_5.txt"],
    )
    with files[0].open(mode="r", encoding="utf-8") as expected_file:
        expected_out = expected_file.read()

    exit_result = main(
        ["latest", "--rating=colley-matrix", "--top=5", f"--config={query_config}"],
    )
    assert exit_result == 0

    captured_out, captured_err = capsys.readouterr()
    assert captured_out == expected_out
    assert captured_err == ""


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


def test_main_games(
    capsys: Any,
    output_path: Path,
    data_path: Path,
    test_path: Path,
    query_config: Path,
) -> None:
    _copy_files(data_path, test_path, ["test_data.db", "test_data.json"])
    files = _copy_files(output_path, test_path, ["main_games.txt"])
    with files[0].open(mode="r", encoding="utf-8") as expected_file:
        expected_out = expected_file.read()

    exit_result = main(["games", f"--config={query_config}"])
    assert exit_result == 0

    captured_out, captured_err = capsys.readouterr()
    assert captured_out == expected_out
    assert captured_err == ""


def test_main_games_year(
    capsys: Any,
    output_path: Path,
    data_path: Path,
    test_path: Path,
    query_config: Path,
) -> None:
    _copy_files(data_path, test_path, ["test_data.db", "test_data.json"])
    files = _copy_files(output_path, test_path, ["main_games_2012.txt"])
    with files[0].open(mode="r", encoding="utf-8") as expected_file:
        expected_out = expected_file.read()

    exit_result = main(["games", "2012", f"--config={query_config}"])
    assert exit_result == 0

    captured_out, captured_err = capsys.readouterr()
    assert captured_out == expected_out
    assert captured_err == ""


def test_main_games_week(
    capsys: Any,
    output_path: Path,
    data_path: Path,
    test_path: Path,
    query_config: Path,
) -> None:
    _copy_files(data_path, test_path, ["test_data.db", "test_data.json"])
    files = _copy_files(output_path, test_path, ["main_games_2012w9.txt"])
    with files[0].open(mode="r", encoding="utf-8") as expected_file:
        expected_out = expected_file.read()

    exit_result = main(["games", "2012w9", f"--config={query_config}"])
    assert exit_result == 0

    captured_out, captured_err = capsys.readouterr()
    assert captured_out == expected_out
    assert captured_err == ""
