"""Youtube videos downloader

This script allows the user to download youtube video from given URL.
It support multiple arguments (TBA)

"""

import click
from . import __version__


@click.command()
@click.version_option(version=__version__)
def main() -> None:
    click.echo("Hello world!")
