"""
file_name = routine.py
Created On: 2024/06/27
Lasted Updated: 2024/06/27
Description: _FILL OUT HERE_
Edit Log:
2024/06/27
    - Created file
"""

# STANDARD LIBRARY IMPORTS
from json import load
from os.path import abspath, dirname, join
from typing import List, TypedDict, Set, cast

# THIRD PARTY LIBRARY IMPORTS

# LOCAL LIBRARY IMPORTS
from src.routines.force_graph_updater.force_graph import ForceGraph
from src.routines.routine_decorator import RoutineDecorator, Seconds


class VaultDataJson(TypedDict):
    """
    The data structure of the vaults object in the vaults json file
    """

    save_name: str
    path: str


class VaultJson(TypedDict):
    """The data structure of the vault json"""

    data_directory: str
    vaults: List[VaultDataJson]


def get_force_graph_list() -> List[ForceGraph]:
    """Get the list of force graph objects from the force graph JSON file."""

    force_graphs: List[ForceGraph] = []
    force_graph_json_directory_path = join(
        dirname(abspath(__file__)), "obsidian_vaults.json"
    )

    # TODO CHECH FOR SAME SAVE NAME

    save_paths: Set[str] = set()
    obsidian_vaults: Set[str] = set()

    with open(
        force_graph_json_directory_path,
        "r",
        encoding="UTF-8",
    ) as file:
        vault_json: VaultJson = load(file)

        data_directory: str = vault_json["data_directory"]
        vaults: List[VaultDataJson] = vault_json["vaults"]

        for vault in vaults:
            save_path: str = join(data_directory, vault["save_name"])

            if save_path in save_paths:
                raise ValueError(f"Duplicate save path: {save_path}")

            save_paths.add(save_path)

            vault_path: str = vault["path"]

            if vault_path in obsidian_vaults:
                raise ValueError(f"Duplicate vault path: {vault_path}")

            obsidian_vaults.add(vault_path)

            force_graph = ForceGraph(save_path, vault_path)
            force_graphs.append(force_graph)

    return force_graphs


@RoutineDecorator(
    task_name="force_graph_routine", routine_metadata={"interval": cast(Seconds, 1800)}
)  # Run every 30 minutes
async def routine() -> None:
    """
    The routine to update the force graph list
    """

    force_graph_list: List[ForceGraph] = get_force_graph_list()

    for force_graph in force_graph_list:
        force_graph.update_force_graph_json()
