"""
file_name = routine.py
Created On: 2024/06/26
Lasted Updated: 2024/06/26
Description: A routine decorator to run a routine function at a specified interval.
Edit Log:
2024/06/26
    - Created file
"""

# STANDARD LIBRARY IMPORTS
from typing import Callable, Set
import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


# THIRD PARTY LIBRARY IMPORTS
from asyncio import sleep

# LOCAL LIBRARY IMPORTS


# class ImmediateFlushTimedRotatingFileHandler(TimedRotatingFileHandler):
#     """A handler class which writes formatted logging records to disk files and flushes immediately."""

#     def emit(self, record):
#         super().emit(record)
#         self.flush()  # Force flush the buffer to disk


class RoutineDecorator:
    """Decorator to run a routine function at a specified interval."""

    _task_names: Set[str] = set()

    def __init__(self, task_name: str, interval: int):
        """Initialize the decorator with the interval."""
        self.task_name = task_name
        self.interval = interval

        self._add_task_name(task_name)

        self.logger = self._setup_logger(task_name)

    def __call__(self, routine_function: Callable):
        """Make the instance callable and return the wrapper function."""

        async def wrapper():
            while True:
                await routine_function()
                await sleep(self.interval)
                self.logger.info("SUCCESS")

        return wrapper

    # PRIVATE FUNCTIONS START HERE
    @classmethod
    def _add_task_name(cls, task_name):
        """Add the task name to the list of task names. If it already exists, raise an error."""

        if task_name in cls._task_names:
            raise ValueError(f"Task name {task_name} already exists.")

        cls._task_names.add(task_name)

    def _setup_logger(self, task_name: str):
        """Setup the logger for the routine function."""
        logger = logging.getLogger(self.task_name)
        logger.setLevel(logging.INFO)

        logging_directory_path = Path(__file__).resolve().parents[2] / "logs"

        if not logger.handlers:
            # Create a TimedRotatingFileHandler that rotates logs daily
            handler = TimedRotatingFileHandler(
                filename=f"{logging_directory_path}/{task_name}.log",  # Log file name
                when="midnight",  # Rotate at midnight
                interval=1,  # Interval is 1 day
            )
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger
