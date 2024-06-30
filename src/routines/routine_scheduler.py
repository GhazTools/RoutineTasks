"""
file_name = routine_scheduler.py
Created On: 2024/06/29
Lasted Updated: 2024/06/29
Description: _FILL OUT HERE_
Edit Log:
2024/06/29
    - Created file
"""

# STANDARD LIBRARY IMPORTS
from datetime import datetime, timedelta, date
from enum import Enum

# THIRD PARTY LIBRARY IMPORTS

# LOCAL LIBRARY IMPORTS


class WeekdayMapper(Enum):
    """
    The datetime weekday associated with a datetime
    """

    MONDAY = date(2023, 1, 2).weekday()  # 2023-01-02 is a Monday
    TUESDAY = date(2023, 1, 3).weekday()
    WEDNESDAY = date(2023, 1, 4).weekday()
    THURSDAY = date(2023, 1, 5).weekday()
    FRIDAY = date(2023, 1, 6).weekday()
    SATURDAY = date(2023, 1, 7).weekday()
    SUNDAY = date(2023, 1, 8).weekday()


class RoutineScheduler:
    """
    A class to handle scheduling of routines
    """

    def __init__(self, day_to_run_on: int, hour_to_run_at: int):
        self._day_to_run_on = day_to_run_on
        self._hour_to_run_at = hour_to_run_at

    def seconds_till_next_run(self) -> int:
        """
        Calculate the number of seconds until the next run of the routine.

        Returns:
            int: The number of seconds till the next routine run.
        """

        next_run_date: datetime = self.get_next_run_date()
        todays_date: datetime = datetime.now()

        return int((next_run_date - todays_date).total_seconds())

    # PRIVATE METHODS START HERE
    def get_next_run_date(self) -> datetime:
        """
        Get the next date where the routine will run based on todays date
        """

        todays_date: datetime = datetime.now()
        current_weekday = todays_date.weekday()
        next_date: datetime

        if current_weekday == self._day_to_run_on:
            next_date = todays_date + timedelta(days=self._day_to_run_on)
        elif current_weekday < self._day_to_run_on:
            next_date = todays_date + timedelta(
                days=self._day_to_run_on - current_weekday
            )
        else:
            next_date = todays_date + timedelta(
                days=7 - current_weekday + self._day_to_run_on
            )

        next_date.replace(hour=self._hour_to_run_at, minute=0, second=0, microsecond=0)
        return next_date
