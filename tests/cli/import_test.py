from pathlib import Path
from typing import Any

from fbsrankings.cli.main import main

from .copy_files import _copy_files


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
