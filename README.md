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
* [__black__](https://github.com/psf/black)_^19.10b0_
* [__flake8__](https://flake8.pycqa.org/en/latest/)_^3.9.2_
* [__pre-commit__](https://pre-commit.com/)_^2.19.0_
* [__mypy__](http://mypy-lang.org/)_^0.961_

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

Add section to existing `~/.bashrc` script or create a new file and add the segment responsible for preparing `pyenv` virtual environment

```bash
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
export PATH="$HOME/.local/bin:$PATH"
```

Next, load all environment variables in current shell script from files

```bash
# To load required environment variables
source ~/.bashrc
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

## Linting, typing and pre-commit hooks

[__Black__](https://github.com/psf/black) is used as a file formatter, configured together with [__Flake8__](https://flake8.pycqa.org/en/latest/) as a tool for enforcing consistent coding style across the project.
Both are defined as a separate stages inside `noxfile.py` (formatting using Black is also done withing linting process with Flake8)
The configuration file for Flake8 is located in the root directory of the project, inside `.flake8` file.
There are also many plugins installed for Flake8, which further enhance the development by providing even more strictness and checks against violation of best code practices:

* `flake8-bandit`
* `flake8-black`
* `flake8-bugbear`
* `flake8-import-order`
* `flake8-comprehensions`
* `flake8-docstrings`
* `flake8-spellcheck`
* `flake8-pytest-style`
* `flake8-pytest`
* `flake8-annotations`

To run black separately:

```bash
# In the root directory
black <path>
```

To run flake8 separately:

```bash
# In the root directory
flake8 --config=.flake8
```

Static type checking is done using [__mypy__](https://mypy.readthedocs.io/en/stable/index.html#). The configuration options are placed within `pyproject.toml` file under `[tool.mypy]` section.

The `.pre-commit-config.yaml` configuration file contains definition of hooks executed using [__pre-commit__](https://pre-commit.com/) before committing the changes to the remote repository.
It defines steps like using black, flake8, static type checks, checking the merge conflicts, trimming railing whitespace etc.

To run the pre-hooks without committing the changes:

```bash
# In the root directory
pre-commit run --all-files
```


## CI/CD

TBA

## Useful links

* <https://cjolowicz.github.io/posts/hypermodern-python-01-setup/> (inspiration for this project)
