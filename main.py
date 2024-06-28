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
from src.routines.routine_list import routine_list


async def main_task() -> None:
    """Main task to setup and run the routine manager."""
    routine_manager: RoutineManager = RoutineManager()

    await routine_manager.register_tasks(tasks=routine_list)
    await routine_manager.run_tasks()

    await sleep(1)


if __name__ == "__main__":
    run(main_task())
