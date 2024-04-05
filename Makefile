.PHONY:
    init
    install
    install-test
    install-dev
    upgrade
    check
    pre-commit
    test
    test-types
    test-coverage
    clean
    build
    upload

init:
    python -m pip install pip --upgrade
    pip install setuptools --upgrade
    pip install wheel --upgrade

init-dev:
    python -m venv env/dev --clear
    env\dev\Scripts\activate
    pip install py-make
    pymake install-dev

install:
    init
    pip install .

install-test:
    init
    pip install .[test]

install-dev:
    init
    pip install -r requirements-dev.txt

upgrade:
    init
    pip-compile --output-file=requirements.txt setup.py --upgrade
    sort-requirements requirements.txt
    python -c "f = open('requirements-dev.in', 'w'); f.write('-e .[dev]'); f.close()"
    pip-compile --output-file=requirements-dev.txt requirements-dev.in --upgrade
    python -c "import os; os.remove('requirements-dev.in')"
    python -c "\
import re; \
p = re.compile('file://[^\r\n]+fbsrankings'); \
filename = 'requirements-dev.txt'; \
f = open(filename); \
file_text = p.sub('.                    ', f.read()); \
f.close(); \
f = open(filename, 'w'); \
f.write(file_text); \
f.close(); "
    sort-requirements requirements-dev.txt
    pip-sync requirements-dev.txt

check:
    black src tests setup.py
    flake8 src tests setup.py
    mypy src tests setup.py
    vulture src tests setup.py
    pylint src tests setup.py
    bandit -r src
    pyroma .

pre-commit:
    pre-commit run --all-files

test:
    pytest tests

test-types:
    pytest tests --typeguard-packages=fbsrankings

test-coverage:
    coverage erase
    coverage run --source=src -m pytest tests
    coverage report

run:
    python -c "from fbsrankings.__main__ import main; main(['import', '2012-2013', '--drop', '--check', '--trace'])"

clean:
    python -c "import shutil; shutil.rmtree('build', True)"
    python -c "import shutil; shutil.rmtree('dist', True)"
    python -c "import shutil; shutil.rmtree('src/fbsrankings.egg-info', True)"
    python -m venv env/install --clear

build:
    clean
    python setup.py sdist bdist_wheel

upload:
    twine upload --repository testpypi dist/*
