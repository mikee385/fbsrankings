from fbsrankings import __version__


def test_installed_version() -> None:
    assert __version__ == "8.0.0-dev.6"
