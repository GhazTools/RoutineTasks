"""
file_name = main.py
Created On: 2024/06/26
Lasted Updated: 2024/06/26
Description: _FILL OUT HERE_
Edit Log:
2024/06/26
    - Created file
"""

# STANDARD LIBRARY IMPORTS

# THIRD PARTY LIBRARY IMPORTS
from asyncio import run, sleep

# LOCAL LIBRARY IMPORTS
from src.routine_manager import RoutineManager
from src.routines.routine_decorator import RoutineDecorator


@RoutineDecorator(interval=1, task_name="perpetual_task_1")
async def perpetual_task():
    print("Task is running...")


@RoutineDecorator(interval=3, task_name="perpetual_task_2")
async def perpetual_task_2():
    print("Ghaz was here...")


async def main_task() -> None:
    """Main task to setup and run the routine manager."""
    routine_manager: RoutineManager = RoutineManager()

    await routine_manager.register_tasks(
        [
            {
                "interval": 1,
                "name": "Perpetual Task",
                "routine_function": perpetual_task,
            },
            {
                "interval": 2,
                "name": "Perpetual Task 2",
                "routine_function": perpetual_task_2,
            },
        ]
    )

    await routine_manager.run_tasks()

    await sleep(1)


if __name__ == "__main__":
    run(main_task())
