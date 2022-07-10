"""Youtube videos downloader


This script allows the user to download youtube video from given URL.

The possible downloaded files, contain both audio and video as a single file (progressive)

"""

import os
import sys

import click
import pytube
import tqdm

from . import __version__


@click.command()
@click.option("--url", help="A YouTube watch URL", required=True, type=str)
@click.option(
    "-r",
    "--resolution",
    help="Resolution of the video to download. If not specified, uses highest resolution possible.",
    required=False,
    type=str,
)
@click.option(
    "-o",
    "--output-path",
    help="Output path for downloaded media file. Defaults to current working directory",
    required=False,
    type=str,
)
@click.option(
    "-f",
    "--filename",
    help="Output filename for downloaded media file. Defaults to the video's filename.",
    required=False,
    type=str,
)
@click.version_option(version=__version__)
def main(url: str, resolution: str, output_path: str, filename: str) -> None:

    try:

        yt = pytube.YouTube(url)

        progressive_streams = yt.streams.filter(progressive=True)

        if not resolution:

            click.secho(
                f"⚠️ No resolution specified. Downloading video in highest resolution possible: {progressive_streams.get_highest_resolution().resolution}",
                fg="yellow",
            )

            stream = progressive_streams.get_highest_resolution()

        else:

            stream = progressive_streams.get_by_resolution(resolution)

            if not stream:

                click.secho(
                    f"⚠️ {resolution} resolution not available for the video. Possible video resolutions: {[stream.resolution for stream in progressive_streams.order_by('resolution')]}",
                    fg="yellow",
                )

                sys.exit(1)

        pbar = tqdm.tqdm(
            total=stream.filesize,
            unit="bytes",
            unit_scale=True,
            unit_divisor=1000,
            desc=filename or stream.title,
        )

        def on_progress(
            stream: pytube.Stream, chunk: bytes, bytes_remaining: int
        ) -> None:

            pbar.update(len(chunk))

        def on_complete(stream: pytube.Stream, file_path: str) -> None:

            pbar.close()

            click.secho(
                f"✔️ File {filename or stream.title} saved at {os.path.normpath(file_path)} in {stream.resolution} resolution.",
                fg="green",
            )

        yt.register_on_progress_callback(on_progress)

        yt.register_on_complete_callback(on_complete)

        stream.download(output_path=output_path, filename=filename)

    except pytube.exceptions.VideoUnavailable:

        click.secho(f"❌ Video {url} is unavailable.", fg="red")

        sys.exit(1)

    except pytube.exceptions.RegexMatchError:

        click.secho(f"❌ URL watch link {url} is invalid.", fg="red")

        sys.exit(1)
