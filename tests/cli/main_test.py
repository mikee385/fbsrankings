# pylint: disable=redefined-outer-name
import json
import os
import shutil
from pathlib import Path
from typing import Any
from typing import List
from typing import Sequence
from typing import Tuple

import pytest

from fbsrankings import __version__
from fbsrankings.cli import main


def _copy_files(src_dir: Path, dest_dir: Path, files: Sequence[str]) -> Sequence[Path]:
    file_paths: List[Path] = []

    for file in files:
        src_path = src_dir / file
        dest_path = dest_dir / file

        shutil.copyfile(src_path, dest_path)
        file_paths.append(dest_path)

    return file_paths


@pytest.fixture()  # type: ignore
def data_path(request: Any) -> Path:
    filename = request.module.__file__
    test_dir = Path(filename).parent.parent
    data_dir = test_dir / "data"
    return data_dir


@pytest.fixture()  # type: ignore
def test_path(tmpdir: Any) -> Path:
    return Path(str(tmpdir))


@pytest.fixture()  # type: ignore
def sqlite_file_config(data_path: Path, test_path: Path) -> Tuple[Path, Path]:
    src_path = data_path / "test_config.json"
    dest_path = test_path / "test_config.json"
    db_path = test_path / "test_data.db"
    with open(src_path) as src_file, open(dest_path, "w") as dest_file:
        src_json = json.load(src_file)
        src_json["storage_type"] = "sqlite"
        src_json["database"] = str(db_path)
        json.dump(src_json, dest_file)
    return dest_path, db_path


@pytest.fixture()  # type: ignore
def sqlite_memory_config(data_path: Path, test_path: Path) -> Path:
    src_path = data_path / "test_config.json"
    dest_path = test_path / "test_config.json"
    with open(src_path) as src_file, open(dest_path, "w") as dest_file:
        src_json = json.load(src_file)
        src_json["storage_type"] = "sqlite"
        src_json["database"] = ":memory:"
        json.dump(src_json, dest_file)
    return dest_path


@pytest.fixture()  # type: ignore
def memory_config(data_path: Path, test_path: Path) -> Path:
    src_path = data_path / "test_config.json"
    dest_path = test_path / "test_config.json"
    with open(src_path) as src_file, open(dest_path, "w") as dest_file:
        src_json = json.load(src_file)
        src_json["storage_type"] = "memory"
        json.dump(src_json, dest_file)
    return dest_path


def test_main_help(
    capsys: Any,
    data_path: Path,
    test_path: Path,
    sqlite_file_config: Tuple[Path, Path],
) -> None:
    files = _copy_files(data_path, test_path, ["main_help.txt"])
    with open(files[0]) as expected_file:
        expected_out = expected_file.read()

    test_config, _ = sqlite_file_config
    with pytest.raises(SystemExit) as exit_result:
        main(["--help", f"--config={test_config}"])
    assert exit_result.type == SystemExit
    assert exit_result.value.code == 0

    captured_out, captured_err = capsys.readouterr()
    assert captured_out == expected_out
    assert captured_err == ""


def test_main_version(capsys: Any, sqlite_file_config: Tuple[Path, Path]) -> None:
    test_config, _ = sqlite_file_config
    with pytest.raises(SystemExit) as exit_result:
        main(["--version", f"--config={test_config}"])
    assert exit_result.type == SystemExit
    assert exit_result.value.code == 0

    captured_out, captured_err = capsys.readouterr()
    assert captured_out == f"{__version__}\n"
    assert captured_err == ""


def test_main_missing_command(
    capsys: Any,
    data_path: Path,
    test_path: Path,
    sqlite_file_config: Tuple[Path, Path],
) -> None:
    files = _copy_files(data_path, test_path, ["main_missing_command.txt"])
    with open(files[0]) as expected_file:
        expected_out = expected_file.read()

    test_config, _ = sqlite_file_config
    with pytest.raises(SystemExit) as exit_result:
        main([f"--config={test_config}"])
    assert exit_result.type == SystemExit
    assert exit_result.value.code == 0

    captured_out, captured_err = capsys.readouterr()
    assert captured_out == expected_out
    assert captured_err == ""


def test_main_invalid_command(
    capsys: Any,
    data_path: Path,
    test_path: Path,
    sqlite_file_config: Tuple[Path, Path],
) -> None:
    files = _copy_files(data_path, test_path, ["main_invalid_command.txt"])
    with open(files[0]) as expected_file:
        expected_err = expected_file.read()

    test_config, _ = sqlite_file_config
    with pytest.raises(SystemExit) as exit_result:
        main(["invalid", f"--config={test_config}"])
    assert exit_result.type == SystemExit
    assert exit_result.value.code == 2

    captured_out, captured_err = capsys.readouterr()
    assert captured_out == ""
    assert captured_err == expected_err


def test_main_import_all_sqlite_file(
    capsys: Any,
    data_path: Path,
    test_path: Path,
    sqlite_file_config: Tuple[Path, Path],
) -> None:
    files = _copy_files(data_path, test_path, ["main_import_all_drop_check.txt"])
    with open(files[0]) as expected_file:
        expected_out = expected_file.read()

    test_config, test_db = sqlite_file_config
    with pytest.raises(SystemExit) as exit_result:
        main(
            [
                "import",
                "all",
                "--drop",
                "--check",
                f"--config={test_config}",
                "--trace",
            ],
        )
    assert exit_result.type == SystemExit
    assert exit_result.value.code == 0

    captured_out, captured_err = capsys.readouterr()
    assert captured_out == expected_out
    assert "Dropping existing data:" in captured_err
    assert "Importing season data:" in captured_err
    assert "Calculating rankings:" in captured_err

    assert os.path.exists(test_db), "Test database is missing"
    assert os.path.isfile(test_db), "Test database is not a file"


def test_main_import_all_sqlite_memory(
    capsys: Any, data_path: Path, test_path: Path, sqlite_memory_config: Path,
) -> None:
    files = _copy_files(data_path, test_path, ["main_import_all_drop_check.txt"])
    with open(files[0]) as expected_file:
        expected_out = expected_file.read()

    with pytest.raises(SystemExit) as exit_result:
        main(
            [
                "import",
                "all",
                "--drop",
                "--check",
                f"--config={sqlite_memory_config}",
                "--trace",
            ],
        )
    assert exit_result.type == SystemExit
    assert exit_result.value.code == 0

    captured_out, captured_err = capsys.readouterr()
    assert captured_out == expected_out
    assert "Dropping existing data:" in captured_err
    assert "Importing season data:" in captured_err
    assert "Calculating rankings:" in captured_err


def test_main_import_all_memory(
    capsys: Any, data_path: Path, test_path: Path, memory_config: Path,
) -> None:
    files = _copy_files(data_path, test_path, ["main_import_all_drop_check.txt"])
    with open(files[0]) as expected_file:
        expected_out = expected_file.read()

    with pytest.raises(SystemExit) as exit_result:
        main(
            [
                "import",
                "all",
                "--drop",
                "--check",
                f"--config={memory_config}",
                "--trace",
            ],
        )
    assert exit_result.type == SystemExit
    assert exit_result.value.code == 0

    captured_out, captured_err = capsys.readouterr()
    assert captured_out == expected_out
    assert "Dropping existing data:" in captured_err
    assert "Importing season data:" in captured_err
    assert "Calculating rankings:" in captured_err


def test_main_seasons(
    capsys: Any,
    data_path: Path,
    test_path: Path,
    sqlite_file_config: Tuple[Path, Path],
) -> None:
    files = _copy_files(data_path, test_path, ["main_seasons.txt", "test_data.db"])
    with open(files[0]) as expected_file:
        expected_out = expected_file.read()

    test_config, _ = sqlite_file_config
    with pytest.raises(SystemExit) as exit_result:
        main(["seasons", f"--config={test_config}"])
    assert exit_result.type == SystemExit
    assert exit_result.value.code == 0

    captured_out, captured_err = capsys.readouterr()
    assert captured_out == expected_out
    assert captured_err == ""


def test_main_latest(
    capsys: Any,
    data_path: Path,
    test_path: Path,
    sqlite_file_config: Tuple[Path, Path],
) -> None:
    files = _copy_files(data_path, test_path, ["main_latest.txt", "test_data.db"])
    with open(files[0]) as expected_file:
        expected_out = expected_file.read()

    test_config, _ = sqlite_file_config
    with pytest.raises(SystemExit) as exit_result:
        main(["latest", f"--config={test_config}"])
    assert exit_result.type == SystemExit
    assert exit_result.value.code == 0

    captured_out, captured_err = capsys.readouterr()
    assert captured_out == expected_out
    assert captured_err == ""


def test_main_latest_rating_srs_top_5(
    capsys: Any,
    data_path: Path,
    test_path: Path,
    sqlite_file_config: Tuple[Path, Path],
) -> None:
    files = _copy_files(
        data_path,
        test_path,
        ["main_latest_rating_colley_matrix_top_5.txt", "test_data.db"],
    )
    with open(files[0]) as expected_file:
        expected_out = expected_file.read()

    test_config, _ = sqlite_file_config
    with pytest.raises(SystemExit) as exit_result:
        main(["latest", "--rating=colley-matrix", "--top=5", f"--config={test_config}"])
    assert exit_result.type == SystemExit
    assert exit_result.value.code == 0

    captured_out, captured_err = capsys.readouterr()
    assert captured_out == expected_out
    assert captured_err == ""


def test_main_teams(
    capsys: Any,
    data_path: Path,
    test_path: Path,
    sqlite_file_config: Tuple[Path, Path],
) -> None:
    files = _copy_files(data_path, test_path, ["main_teams.txt", "test_data.db"])
    with open(files[0]) as expected_file:
        expected_out = expected_file.read()

    test_config, _ = sqlite_file_config
    with pytest.raises(SystemExit) as exit_result:
        main(["teams", f"--config={test_config}"])
    assert exit_result.type == SystemExit
    assert exit_result.value.code == 0

    captured_out, captured_err = capsys.readouterr()
    assert captured_out == expected_out
    assert captured_err == ""


def test_main_teams_year(
    capsys: Any,
    data_path: Path,
    test_path: Path,
    sqlite_file_config: Tuple[Path, Path],
) -> None:
    files = _copy_files(data_path, test_path, ["main_teams_2012.txt", "test_data.db"])
    with open(files[0]) as expected_file:
        expected_out = expected_file.read()

    test_config, _ = sqlite_file_config
    with pytest.raises(SystemExit) as exit_result:
        main(["teams", "2012", f"--config={test_config}"])
    assert exit_result.type == SystemExit
    assert exit_result.value.code == 0

    captured_out, captured_err = capsys.readouterr()
    assert captured_out == expected_out
    assert captured_err == ""


def test_main_teams_week(
    capsys: Any,
    data_path: Path,
    test_path: Path,
    sqlite_file_config: Tuple[Path, Path],
) -> None:
    files = _copy_files(data_path, test_path, ["main_teams_2012w9.txt", "test_data.db"])
    with open(files[0]) as expected_file:
        expected_out = expected_file.read()

    test_config, _ = sqlite_file_config
    with pytest.raises(SystemExit) as exit_result:
        main(["teams", "2012w9", f"--config={test_config}"])
    assert exit_result.type == SystemExit
    assert exit_result.value.code == 0

    captured_out, captured_err = capsys.readouterr()
    assert captured_out == expected_out
    assert captured_err == ""


def test_main_games(
    capsys: Any,
    data_path: Path,
    test_path: Path,
    sqlite_file_config: Tuple[Path, Path],
) -> None:
    files = _copy_files(data_path, test_path, ["main_games.txt", "test_data.db"])
    with open(files[0]) as expected_file:
        expected_out = expected_file.read()

    test_config, _ = sqlite_file_config
    with pytest.raises(SystemExit) as exit_result:
        main(["games", f"--config={test_config}"])
    assert exit_result.type == SystemExit
    assert exit_result.value.code == 0

    captured_out, captured_err = capsys.readouterr()
    assert captured_out == expected_out
    assert captured_err == ""


def test_main_games_year(
    capsys: Any,
    data_path: Path,
    test_path: Path,
    sqlite_file_config: Tuple[Path, Path],
) -> None:
    files = _copy_files(data_path, test_path, ["main_games_2012.txt", "test_data.db"])
    with open(files[0]) as expected_file:
        expected_out = expected_file.read()

    test_config, _ = sqlite_file_config
    with pytest.raises(SystemExit) as exit_result:
        main(["games", "2012", f"--config={test_config}"])
    assert exit_result.type == SystemExit
    assert exit_result.value.code == 0

    captured_out, captured_err = capsys.readouterr()
    assert captured_out == expected_out
    assert captured_err == ""


def test_main_games_week(
    capsys: Any,
    data_path: Path,
    test_path: Path,
    sqlite_file_config: Tuple[Path, Path],
) -> None:
    files = _copy_files(data_path, test_path, ["main_games_2012w9.txt", "test_data.db"])
    with open(files[0]) as expected_file:
        expected_out = expected_file.read()

    test_config, _ = sqlite_file_config
    with pytest.raises(SystemExit) as exit_result:
        main(["games", "2012w9", f"--config={test_config}"])
    assert exit_result.type == SystemExit
    assert exit_result.value.code == 0

    captured_out, captured_err = capsys.readouterr()
    assert captured_out == expected_out
    assert captured_err == ""
