from datetime import timedelta

class Result:
    delta: timedelta | None
    wpm: int | None
    def __init__(self, seconds: int | None = ..., wpm: int | None = ...) -> None: ...
    def __unicode__(self) -> str: ...
    @property
    def seconds(self) -> int: ...
    @property
    def minutes(self) -> int: ...
    @property
    def text(self) -> str: ...
    def total_seconds(self, delta: timedelta) -> int: ...