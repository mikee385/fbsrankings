import setuptools

from fbsrankings import __author__
from fbsrankings import __version__

with open("README.md") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fbsrankings",
    version=__version__,
    author=__author__,
    author_email="mikee385@gmail.com",
    description="Import college football teams and games from sportsreference.com and calculate rankings for the Division I Football Bowl Subdivision (FBS) teams",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mikee385/fbsrankings",
    packages=["fbsrankings"],
    license="MIT",
    classifiers=[
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
    install_requires=[
        "bs4",
        "html5lib",
        "jsonschema",
        "numpy",
        "prettytable",
        "tqdm",
        "typing-extensions",
    ],
    entry_points={"console_scripts": ["fbsrankings=fbsrankings.cli.main:main"]},
)
