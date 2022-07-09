import os
from pathlib import Path
from typing import Dict, List

import click.testing
from click.testing import CliRunner
import pytest
from pytest_mock import MockerFixture
from src.youtube_downloader import cli

from .stubs import MockStreamsArray, MockYoutube

urls_fixture: Dict[str, List[str]] = {
    "invalid-urls": [
        "http://bone.example.com/?branch=beef&advertisement=border",
        "http://www.example.org/?birth=badge",
        "https://www.youtube.com/watch?v=YYJbJOTdZB",
        "https://www.youtube.com/watch?v=YoJO9dZBX1",
    ],
    "unavailable-urls": [
        "https://www.youtube.com/watch?v=XaJOTdZBX11",
        "https://www.youtube.com/watch?v=YbJOTdZBX10",
        "https://www.youtube.com/watch?v=ZcJOTdZBX1q",
    ],
}

VALID_URL: str = "https://www.youtube.com/watch?v=YbJOTdZBX1g"


@pytest.fixture(autouse=True)
def cli_runner() -> CliRunner:
    return click.testing.CliRunner()


@pytest.mark.unit()
def test_main_missing_url(cli_runner: CliRunner):
    result = cli_runner.invoke(cli.main)
    assert result.exit_code == 2


@pytest.mark.unit()
@pytest.mark.parametrize("url", urls_fixture["invalid-urls"])
def test_main_invalid_url(cli_runner: CliRunner, url: str) -> None:

    result = cli_runner.invoke(cli.main, ["--url", url])
    assert result.exit_code == 1
    assert f"❌ URL watch link {url} is invalid." in result.output


@pytest.mark.unit()
@pytest.mark.parametrize("url", urls_fixture["unavailable-urls"])
def test_main_video_unavailable(cli_runner: CliRunner, url: str) -> None:
    result = cli_runner.invoke(cli.main, ["--url", url])
    assert result.exit_code == 1
    assert f"❌ Video {url} is unavailable." in result.output


@pytest.mark.unit()
def test_main_no_resolution_provided(
    cli_runner: CliRunner, mocker: MockerFixture
) -> None:
    import pytube
    import tqdm

    mocker.patch.object(tqdm, "tqdm")
    mocker.patch.object(pytube, "YouTube").return_value = MockYoutube()

    result = cli_runner.invoke(cli.main, ["--url", VALID_URL])
    assert result.exit_code == 0
    assert (
        "⚠️ No resolution specified. Downloading video in highest resolution possible: 720p"
        in result.output
    )


@pytest.mark.unit()
@pytest.mark.parametrize(
    "arguments",
    [
        ["--url", VALID_URL, "-r", "invalid"],
        ["--url", VALID_URL, "--resolution", "invalid"],
    ],
)
def test_main_invalid_resolution(
    cli_runner: CliRunner, mocker: MockerFixture, arguments: List[str]
) -> None:
    import pytube
    import tqdm

    mocker.patch.object(tqdm, "tqdm")
    mocker.patch.object(MockStreamsArray, "get_by_resolution").return_value = None
    mocker.patch.object(pytube, "YouTube").return_value = MockYoutube()
    result = cli_runner.invoke(cli.main, ["--url", VALID_URL, *arguments])
    assert result.exit_code == 1
    assert (
        "⚠️ invalid resolution not available for the video. Possible video resolutions: ['144p', '360p', '720p']"
        in result.output
    )


@pytest.mark.e2e()
def test_main_success_e2e_download_default_options(cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(cli.main, ["--url", VALID_URL])
    assert result.exit_code == 0
    assert os.path.isfile(
        "YouTube Rewind 2018 Everyone Controls Rewind  YouTubeRewind.mp4"
    )
    assert (
        f"✔️ File YouTube Rewind 2018: Everyone Controls Rewind | #YouTubeRewind saved at {os.getcwd()}/YouTube Rewind 2018 Everyone Controls Rewind  YouTubeRewind.mp4 in 720p resolution."
        in result.output
    )
    os.remove("./YouTube Rewind 2018 Everyone Controls Rewind  YouTubeRewind.mp4")


@pytest.mark.e2e()
@pytest.mark.parametrize("argument", ["-o", "--output-path"])
def test_main_success_e2e_download_custom_path(
    cli_runner: CliRunner, argument: str, tmp_path: Path
) -> None:
    result = cli_runner.invoke(
        cli.main, ["--url", VALID_URL, argument, str(tmp_path.cwd())]
    )
    assert result.exit_code == 0
    assert os.path.isfile(
        os.path.join(
            tmp_path.cwd(),
            "YouTube Rewind 2018 Everyone Controls Rewind  YouTubeRewind.mp4",
        )
    )
    assert (
        f"✔️ File YouTube Rewind 2018: Everyone Controls Rewind | #YouTubeRewind saved at {tmp_path.cwd()}/YouTube Rewind 2018 Everyone Controls Rewind  YouTubeRewind.mp4 in 720p resolution."
        in result.output
    )


@pytest.mark.e2e()
@pytest.mark.parametrize(
    "arguments", [["-f", "file-1.mp4"], ["--filename", "file-2.mp4"]]
)
def test_main_success_e2e_download_custom_filename(
    cli_runner: CliRunner, arguments: List[str]
) -> None:
    result = cli_runner.invoke(cli.main, ["--url", VALID_URL, *arguments])
    assert result.exit_code == 0
    assert os.path.isfile(arguments[1])
    assert (
        f"✔️ File {arguments[1]} saved at {os.getcwd()}/{arguments[1]} in 720p resolution."
        in result.output
    )
    os.remove(f"{os.getcwd()}/{arguments[1]}")


@pytest.mark.e2e()
@pytest.mark.parametrize(
    "arguments",
    [
        ["-r", "360p", "-o", "./"],
        ["--resolution", "720p", "-o", "./"],
        ["-r", "360p", "--output-path", "./"],
        ["--resolution", "360p", "--output-path", "./"],
        ["-r", "360p", "-f", "file.mp4"],
        ["--resolution", "720p", "-f", "file.mp4"],
        ["-r", "360p", "--filename", "file.mp4"],
        ["--resolution", "360p", "--filename", "file.mp4"],
        ["-o", "./", "-f", "file.mp4"],
        ["--output-path", "./", "-f", "file.mp4"],
        ["-o", "./", "--filename", "file.mp4"],
        ["--output-path", "./", "--filename", "file.mp4"],
        ["--resolution", "720p", "--output-path", "./", "--filename", "file.mp4"],
        ["-r", "720p", "-o", "./", "-f", "file.mp4"],
    ],
)
def test_main_success_e2e_download_different_parameters(
    cli_runner: CliRunner, arguments: List[str]
) -> None:
    result = cli_runner.invoke(cli.main, ["--url", VALID_URL, *arguments])
    assert result.exit_code == 0

    file_title = (
        "file.mp4"
        if "-f" in arguments or "--filename" in arguments
        else "YouTube Rewind 2018: Everyone Controls Rewind | #YouTubeRewind"
    )

    file_name = (
        "file.mp4"
        if "-f" in arguments or "--filename" in arguments
        else "YouTube Rewind 2018 Everyone Controls Rewind  YouTubeRewind.mp4"
    )

    resolution = "720p"
    if "-r" in arguments:
        resolution = arguments[arguments.index("-r") + 1]

    elif "--resolution" in arguments:
        resolution = arguments[arguments.index("--resolution") + 1]

    assert os.path.isfile(file_name)
    assert (
        f"✔️ File {file_title} saved at {os.getcwd()}/{file_name} in {resolution} resolution."
        in result.output
    )
    os.remove(f"{os.getcwd()}/{file_name}")
