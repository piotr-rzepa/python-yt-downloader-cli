from typing import Any, List


class MockStream:
    def __init__(self, res: str, file: str, title: str) -> None:
        self.resolution = res
        self.filesize = file
        self.title = title

    def download(self, *args: str, **kwargs: Any) -> None:
        pass


class MockStreamsArray:
    def __init__(self) -> None:
        pass
        self.streams = [
            MockStream("144p", "file-144p", "file-title-144p"),
            MockStream("360p", "file-360p", "file-title-360p"),
            MockStream("720p", "file-720p", "file-title-720p"),
        ]

    def filter(self, *args: str, **kwargs: Any):
        return self

    def get_highest_resolution(self) -> MockStream:
        return self.streams[-1]

    def get_by_resolution(self, *args, **kwargs) -> MockStream:
        return self.streams[0]

    def order_by(self, *args, **kwargs) -> List[MockStream]:
        return self.streams


class MockYoutube:
    def __init__(self, *args: str, **kwargs: Any) -> None:
        self.streams = MockStreamsArray()

    def register_on_progress_callback(self, *args: str, **kwargs: Any) -> None:
        pass

    def register_on_complete_callback(self, *args: str, **kwargs: Any) -> None:
        pass
