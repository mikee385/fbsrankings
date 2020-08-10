.PHONY:
    init
    setup
    upgrade
    check
    pre-commit
    clean
    build
    install
    upload

init:
    python -m pip install pip --upgrade
    pip install setuptools --upgrade
    pip install wheel --upgrade

setup:
    init
    pip install -r requirements-dev.txt

upgrade:
    pip-compile --output-file=requirements.txt setup.py --upgrade
    sort-requirements requirements.txt
    pip-compile --output-file=requirements-dev.txt requirements-dev.in --upgrade
    python -c "import re; p = re.compile('file://[^\r\n]+fbsrankings'); filename = 'requirements-dev.txt'; f = open(filename); file_text = p.sub('.                    ', f.read()); f.close(); f = open(filename, 'w'); f.write(file_text); f.close();"
    sort-requirements requirements-dev.txt
    pip-sync requirements-dev.txt

check:
    black src/fbsrankings
    flake8 src/fbsrankings
    pylint src/fbsrankings
    bandit -r src/fbsrankings
    pyroma .
    mypy src/fbsrankings

pre-commit:
    pre-commit run --all-files

clean:
    python -c "import shutil; shutil.rmtree('build', True)"
    python -c "import shutil; shutil.rmtree('dist', True)"
    python -c "import shutil; shutil.rmtree('src/fbsrankings.egg-info', True)"
    python -m venv env/install --clear

build:
    clean
    python setup.py sdist bdist_wheel

install:
    init
    pip install .

upload:
    twine upload --repository testpypi dist/*
