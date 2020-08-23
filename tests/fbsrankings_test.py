from fbsrankings import __version__


def test_installed_version() -> None:
    assert __version__ == "7.0.0-dev.4"
