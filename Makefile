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
    pip-compile --output-file=requirements.txt setup.py --upgrade
    sort-requirements requirements.txt
    pip-compile --output-file=requirements-dev.txt requirements-dev.in --upgrade
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
    pylint src tests setup.py
    bandit -r src
    pyroma .
    mypy src tests setup.py

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
