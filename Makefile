python_version = Python36

.PHONY:
    init
    init-dev
    install
    install-test
    upgrade
    check
    pre-commit
    test
    test-types
    test-coverage
    run
    profile
    clean
    build
    upload

init:
    python -m pip install pip --upgrade
    pip install setuptools --upgrade
    pip install wheel --upgrade

init-dev:
    python -m venv env/$(python_version)/dev --clear
    env\$(python_version)\dev\Scripts\activate
    python -m pip install pip --upgrade
    pip install setuptools wheel py-make pip-tools sort-requirements --upgrade
    upgrade

install:
    init
    pip install .

install-test:
    init
    pip install .[test]

upgrade:
    init
    pip-compile --output-file=requirements/$(python_version).txt setup.py --upgrade
    sort-requirements requirements/$(python_version).txt
    pip-compile --extra=dev --output-file=requirements/$(python_version)-dev.txt setup.py --upgrade
    sort-requirements requirements/$(python_version)-dev.txt
    pip-sync requirements/$(python_version)-dev.txt
    pip install -e .

check:
    isort src tests setup.py
    black src tests setup.py
    flake8 src tests setup.py
    mypy src tests setup.py
    vulture src tests setup.py whitelist.py
    pylint src tests setup.py
    bandit --ini setup.cfg -r src
    pyroma .

pre-commit:
    pre-commit run --all-files

test:
    pytest tests -v

test-types:
    pytest tests -v --typeguard-packages=fbsrankings

test-coverage:
    coverage erase
    coverage run --source=src -m pytest tests -v
    coverage report

run:
    fbsrankings import 2012-2013 --drop --check --trace

profile:
    python -c "import cProfile; from fbsrankings.cli.main import main; cProfile.run(\"main(['import', '2012-2013', '--drop', '--check'])\", \".profiling\")"
    python -c "import pstats; stats = pstats.Stats('.profiling').sort_stats('cumtime'); stats.print_stats()"

clean:
    python -c "import shutil; shutil.rmtree('build', True)"
    python -c "import shutil; shutil.rmtree('dist', True)"
    python -c "import shutil; shutil.rmtree('src/fbsrankings.egg-info', True)"
    python -m venv env/$(python_version)/install --clear

build:
    clean
    python setup.py sdist bdist_wheel

upload:
    twine upload --repository testpypi dist/*
