"""Mock implementations of pytube's classes."""

from typing import Any, List


class MockStream:
    """Mock implementation of pytube's Stream class."""

    def __init__(self, res: str, file: str, title: str) -> None:
        """Inits Stream with resolution, file name and title."""
        self.resolution = res
        self.filesize = file
        self.title = title

    def download(self, *args: str, **kwargs: Any) -> None:
        """Performs empty download functionality for testing purposes."""
        pass


class MockStreamsArray:
    """Mock implementation of pytube's StreamArray class."""

    def __init__(self) -> None:
        """Inits StreamArray with deterministic array of MockStream objects."""
        self.streams = [
            MockStream("144p", "file-144p", "file-title-144p"),
            MockStream("360p", "file-360p", "file-title-360p"),
            MockStream("720p", "file-720p", "file-title-720p"),
        ]

    def filter(self, *args: str, **kwargs: Any):
        """Returns instance of object calling this method for testing purposes."""
        return self

    def get_highest_resolution(self) -> MockStream:
        """Returns last MockStream object for testing purposes."""
        return self.streams[-1]

    def get_by_resolution(self, *args, **kwargs) -> MockStream:
        """Returns first MockStream object for testing purposes."""
        return self.streams[0]

    def order_by(self, *args, **kwargs) -> List[MockStream]:
        """Returns an array of MockStream objects."""
        return self.streams


class MockYoutube:
    """Mock implementation of pytube's Youtube class."""

    def __init__(self, *args: str, **kwargs: Any) -> None:
        """Inits MockYoutube with MockStreamsArray class."""
        self.streams = MockStreamsArray()

    def register_on_progress_callback(self, *args: str, **kwargs: Any) -> None:
        """Mocks callback executed on each video chunk downloaded."""
        pass

    def register_on_complete_callback(self, *args: str, **kwargs: Any) -> None:
        """Mocks callback executed at the end of video download."""
        pass
