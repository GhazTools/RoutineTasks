"""
file_name = routine.py
Created On: 2024/06/29
Lasted Updated: 2024/06/29
Description: _FILL OUT HERE_
Edit Log:
2024/06/29
    - Created file
"""

# STANDARD LIBRARY IMPORTS
from os.path import join, dirname, abspath
from subprocess import run, CalledProcessError
from logging import getLogger, Logger

# THIRD PARTY LIBRARY IMPORTS

# LOCAL LIBRARY IMPORTS
from src.routines.routine_decorator import RoutineDecorator
from src.routines.routine_scheduler import RoutineScheduler, WeekdayMapper

TASK_NAME = "service_restarter_routine"


@RoutineDecorator(
    task_name="service_restarter_routine",
    routine_metadata={"interval": RoutineScheduler(WeekdayMapper.SUNDAY.value, 0)},
)  # Run every 30 minutes
async def routine() -> None:
    """
    A routine to restart all services at the end of the week at 12AM
    """

    service_list_path = join(dirname(abspath(__file__)), "service_list.txt")

    with open(service_list_path, "r", encoding="UTF-8") as file:
        for service_name in file:
            service_name = service_name.strip()
            # Restart the service

            logger = getLogger(TASK_NAME)
            try:
                # Restart the service using systemctl
                run(["sudo", "systemctl", "restart", service_name], check=True)
                logger.info("Successfully restarted %s", service_name)
            except CalledProcessError:
                logger.error("Failed to restart %s", service_name)
