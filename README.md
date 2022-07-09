# python-yt-downloader-cli

Command line interface written in python for downloading youtube videos.
Supports downloading multiple videos asynchronously.
Created with compatibility for _python 3.10.5_ and _3.9.13_

## Dependencies

* [__pyenv__](https://github.com/pyenv/pyenv)_^2.3.1_
* [__click__](https://click.palletsprojects.com/en/8.1.x/)_^8.1.3_
* [__pytube__](https://pytube.io/en/latest/index.html)_^12.1.0_
* [__tqdm__](https://tqdm.github.io/)_^4.64.0_
* [__pytest__](https://docs.pytest.org/en/latest/)_^7.1.1_
* [__coverage[toml]__](https://coverage.readthedocs.io/en/6.4.1/)_^6.4.1_
* [__pytest-cov__](https://pytest-cov.readthedocs.io/en/latest/)_^3.0.0_
* [__pytest-mock__](https://pytest-mock.readthedocs.io/en/latest/)_^3.8.1_
* [__Nox__](https://nox.thea.codes/en/stable/)_^2022.1.7_

## Setup

### Installing pyenv

To manage Python version used for the developer environment, the Python version manager [__pyenv__](https://github.com/pyenv/pyenv) is a tool of choice for the project.

After successfully installing _pyenv_, the specified version of python can be added using following command:

```bash
# pyenv install <PYTHON_RELEASE>
pyenv install 3.10.5
pyenv install 3.9.13
```

Set installed release as application-specific by writing version to `.python-version` file:

```bash
# pyenv local <INSTALLED_PYTHON_RELEASES>
pyenv local 3.10.5 3.9.13
```

The default version is _Python 3.10.5_, to access specific version, `python3.10` and `python3.9` can be used.

```bash
# Output: Python 3.10.5
python3.10 --version

# Output: Python 3.9.13
python3.9 --version
```

### Using Python dependency manager

[__Poetry__](https://python-poetry.org/docs/) is a tool used for dependency management and packaging for the project. It will manage installation and updating of declared libraries.

After installing _Poetry_, initialize Python project as follows:

```bash
# To load required environment variables
source ~/.poetry/env

poetry init -- no-interaction # To skip questions
```

This will create `pyproject.toml` configuration file, which contains the project's package configuration.

Poetry will manage the virtual environment for the project, where all the dependencies as well as specific Python version is locked in an isolated environment.

```bash
# In the working directory
poetry install
```

It will create a virtual environment for the project.

## Testing

Tests are written using [_pytest_](https://docs.pytest.org/en/latest/) framework, installed as dev dependency.
Apart from the framework, [click testing module](https://click.palletsprojects.com/en/8.1.x/testing/#basic-testing) is used to check behavior of invoked command line, and [pytest-mock](https://pytest-mock.readthedocs.io/en/latest/) plugin is used to replace parts of pytube functionalities with custom written mock classes with controlled output.
The source code coverage is measured using [Coverage.py](https://coverage.readthedocs.io/en/6.4.1/) tool, together with [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/) plugin, which integrates _Coverage.py_ with _pytest_.  
Configuration options for _Coverage.py_ are located inside `pyproject.toml` file, within sections marked with `[tool.coverage:<option>]`.  
To perform automatic testing of the CLI in different Python environment, the [Nox](https://nox.thea.codes/en/stable/) tool is being used. It's not installed using _Poetry_ but _pip_, because it will create environment which will install _Poetry_ inside it separately.  
Nox configuration is done via `noxfile.py`, located in project's directory. By default, it creates two different Python environments, with following versions: _3.10_ and _3.9_.

### Run all test cases (unit + e2e)

```bash
poetry run pytest -vvv
```

### Run unit tests exclusively

```bash
poetry run pytest -vvv -m "unit"
```

### Run end-to-end tests exclusively

```bash
poetry run pytest -vvv -m "e2e"
```

### Run tests with coverage report

```bash
poetry run pytest -vvv --cov
```

### Run nox (automated testing in different python environments)

```bash
nox
```

### Run nox, passing additional arguments to the pytest tool (verbose + coverage)

```bash
nox -- -vvv --cov
```

## Linting and typing

TBA

## CI/CD

TBA

## Useful links

* <https://cjolowicz.github.io/posts/hypermodern-python-01-setup/> (inspiration for this project)
