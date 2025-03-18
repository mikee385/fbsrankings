from configparser import ConfigParser
from pathlib import Path
from typing import Any

import pytest


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


@pytest.fixture(name="config_path")
def config_path_fixure(request: Any) -> Path:
    filename = request.module.__file__
    test_dir = Path(filename).parent.parent
    return test_dir / "config"


@pytest.fixture(name="data_path")
def data_path_fixure(request: Any) -> Path:
    filename = request.module.__file__
    test_dir = Path(filename).parent.parent
    return test_dir / "data"


@pytest.fixture(name="output_path")
def output_path_fixure(request: Any) -> Path:
    filename = request.module.__file__
    test_dir = Path(filename).parent.parent
    return test_dir / "output"


@pytest.fixture(name="test_path")
def test_path_fixure(tmpdir: Any) -> Path:
    return Path(str(tmpdir))


@pytest.fixture(name="option_config", params=["memory.ini"])
def option_config_fixure(request: Any, config_path: Path, test_path: Path) -> Path:
    return _build_config_file(config_path, request.param, test_path)


@pytest.fixture(
    name="command_config",
    params=["memory.ini", "sqlite.ini", "tinydb.ini"],
)
def command_config_fixure(request: Any, config_path: Path, test_path: Path) -> Path:
    return _build_config_file(config_path, request.param, test_path)


@pytest.fixture(name="query_config", params=["sqlite.ini", "tinydb.ini"])
def query_config_fixure(request: Any, config_path: Path, test_path: Path) -> Path:
    return _build_config_file(config_path, request.param, test_path)


@pytest.fixture(name="test_seasons")
def test_seasons_fixure() -> list[str]:
    return ["2012", "2013"]
