"""
file_name = routine_scheduler.py
Created On: 2024/06/26
Lasted Updated: 2024/06/26
Description: _FILL OUT HERE_
Edit Log:
2024/06/26
    - Created file
"""

# STANDARD LIBRARY IMPORTS
from typing import Callable, List, TypedDict

# THIRD PARTY LIBRARY IMPORTS
from asyncio import create_task, Task, CancelledError, gather

# LOCAL LIBRARY IMPORTS


class RoutineManager:
    def __init__(self) -> None:
        self.tasks: List[Task] = []

    async def register_tasks(self, tasks: List[Callable]) -> None:
        """Register the tasks to the task list."""
        for task in tasks:
            created_task = create_task(task())
            self.tasks.append(created_task)

    async def run_tasks(self):
        """Run all the tasks in the task list."""

        await gather(*self.tasks)

    async def __aexit__(self, exc_type, exc, tb):
        """Cancel all the tasks if the context manager is exited."""
        for task in self.tasks:
            self._cancel_task(task)
            await task

    # PRIVATE METHODS START HERE
    async def _cancel_task(self, task: Task) -> bool:
        """Cancel the task if it's not done yet."""
        if not task.done():
            task.cancel()
            try:
                await task
            except CancelledError:
                return False

        return True
