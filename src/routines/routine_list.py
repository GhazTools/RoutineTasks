"""
file_name = routine_list.py
Created On: 2024/06/27
Lasted Updated: 2024/06/27
Description: _FILL OUT HERE_
Edit Log:
2024/06/27
    - Created file
"""

# STANDARD LIBRARY IMPORTS
from typing import List, Callable

# THIRD PARTY LIBRARY IMPORTS

# LOCAL LIBRARY IMPORTS
from src.routines.force_graph_updater.routine import routine as force_graph_routine
# from src.routines.restart_services.routine import routine as restart_services


routine_list: List[Callable] = [force_graph_routine]
