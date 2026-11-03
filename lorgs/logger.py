"""Define and setup Logger-Instances."""

import datetime
import logging
import os
import time
from typing import Self


LOG_FORMAT = "[%(reltime)s][%(name)s] %(levelname)s: [%(funcName)s] %(message)s"
"""str: Format to be used for log messages."""


class DeltaTimeFormatter(logging.Formatter):
    def format(self, record):
        duration = datetime.datetime.fromtimestamp(record.relativeCreated / 1000, datetime.UTC)
        record.reltime = duration.strftime("%M:%S.%f")[:7]

        # add a custom "funcName" so we can overwrite it if needed
        if "funcNameCustom" in record.__dict__:
            record.funcName = record.__dict__["funcNameCustom"]

        return super().format(record)


logger = logging.getLogger("Lorgs")
"""The logger to log logging related log messages."""

formatter = DeltaTimeFormatter(LOG_FORMAT)

# Lambda logs whatever reaches the root logger. A handler here would write every line a second time.
if not os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

if os.getenv("DEBUG"):
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)


class Timer:
    def __init__(self, name: str, *, print_on_exit=True) -> None:
        self.name = name
        self.start_time: float = 0
        self.elapsed_time: float = 0
        self.print_on_exit = print_on_exit

    def print(self) -> None:
        extra = {"funcNameCustom": self.name}  # add custom funcName for our LoggerFormatter
        logger.info(f"{self.elapsed_time * 1000:.02f}ms", extra=extra)

    def __enter__(self) -> Self:
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.elapsed_time = time.time() - self.start_time
        if self.print_on_exit:
            self.print()
