from fbsrankings import __version__


def test_installed_version() -> None:
    assert __version__ == "11.0.0-beta"
