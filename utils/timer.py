import time
from .logger import root_logger


class Timer:
    __slots__ = ["fmt", "cost", "start", "display"]

    def __init__(self, fmt: str = "Finished, Cost: %time%", display: bool = False):
        self.fmt = fmt
        self.cost = 0.0
        self.display = display

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cost = time.time() - self.start
        if self.display:
            root_logger.notice(self.fmt.replace("%time%", "{:.2f}s".format(self.cost)))
