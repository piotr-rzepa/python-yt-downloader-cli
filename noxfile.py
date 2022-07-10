"""Nox configuration file for running stages in different python environments."""

import tempfile
from typing import Any, Tuple

import nox
from nox.sessions import Session

# Exclude Black from the session run -> code style is checked within lint stage
nox.options.sessions = ("lint", "mypy_type_check", "tests", "docs")

LOCATIONS: Tuple[str, str, str] = ("src", "tests", "noxfile.py")


def install_from_requirements(session: Session, *args: str, **kwargs: Any) -> None:
    """Installs required packages from requirements.txt."""
    with tempfile.NamedTemporaryFile() as requirements_txt:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements_txt.name}",
            external=True,
        )
        session.install(f"--constraint={requirements_txt.name}", *args, **kwargs)


@nox.session(python=["3.10", "3.9"])
def mypy_type_check(session: Session) -> None:
    """Runs static type checking using mypy."""
    args = session.posargs or LOCATIONS
    install_from_requirements(session, "mypy")
    session.run("mypy", *args)


@nox.session(python=["3.10", "3.9"])
def black(session: Session) -> None:
    """Runs formatting check using black."""
    args = session.posargs or LOCATIONS
    install_from_requirements(session, "black")
    session.run("black", *args)


@nox.session(python=["3.10", "3.9"])
def lint(session: Session) -> None:
    """Runs linting check using flake8 with various plugins."""
    args = session.posargs or LOCATIONS
    install_from_requirements(
        session,
        "flake8",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-import-order",
        "flake8-comprehensions",
        "flake8-docstrings",
        "flake8-spellcheck",
        "flake8-pytest-style",
        "flake8-pytest",
        "darglint",
    )
    session.run("flake8", *args)


@nox.session(python=["3.10", "3.9"])
def tests(session: Session) -> None:
    """Executes test cases (unit + e2e) with coverage report using pytest and coverage.py."""
    args = session.posargs or ["--cov", "-vvv"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_from_requirements(
        session, "coverage[toml]", "pytest", "pytest-cov", "pytest-mock"
    )
    session.run("pytest", *args)


@nox.session(python=["3.10", "3.9"])
def docs(session: Session) -> None:
    """Builds the documentation for the project."""
    session.run("poetry", "install", "--no-dev", external=True)
    install_from_requirements(session, "sphinx", "sphinx-autodoc-typehints")
    session.run("sphinx-build", "docs", "docs/_build")


@nox.session(python=["3.10", "3.9"])
def coverage(session: Session) -> None:
    """Uploads coverage data."""
    install_from_requirements(session, "coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)
