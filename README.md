# python-yt-downloader-cli

Command line interface written in python for downloading youtube videos.
Supports downloading multiple videos asynchronously.
Created with compatibility for _python 3.10.5_ and _3.9.13_

## Dependencies

* [__pyenv__](https://github.com/pyenv/pyenv)_^2.3.1_
* [__click__](https://click.palletsprojects.com/en/8.1.x/)_^8.1.3_

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

TBA

## Linting and typing

TBA

## CI/CD

TBA

## Useful links

* <https://cjolowicz.github.io/posts/hypermodern-python-01-setup/> (inspiration for this project)
