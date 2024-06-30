"""
file_name = force_graph.py
Created On: 2024/06/26
Lasted Updated: 2024/06/26
Description: _FILL OUT HERE_
Edit Log:
2024/06/26
    - Created file
"""

# STANDARD LIBRARY IMPORTS
from json import dump, load, JSONDecodeError
from os import listdir, walk, remove
from os.path import isdir, join, exists, getmtime, abspath, dirname
from re import findall
from subprocess import run, CalledProcessError
from typing import Dict, List, Set, Tuple, TypedDict

# THIRD PARTY LIBRARY IMPORTS

# LOCAL LIBRARY IMPORTS


class GetAllFilesResult(TypedDict):
    """The result of the get_all_files method"""

    md_files: Dict[str, str]
    other_files: Set[Tuple[str, str]]


class ForceGraphNodeData(TypedDict):
    """The data structure of the force graph JSON file."""

    id: str
    name: str
    val: int


class AddForcegraphResult(TypedDict):
    """The result of the add_force_graph method."""

    force_graph_node_data: List[ForceGraphNodeData]
    last_index: int


class ForceGraph:
    """A class to update the force graph JSON file."""

    folders_to_ignore: Set[str] = {".obsidian", ".git"}
    files_to_ignore: Set[str] = {".DS_Store", "Budgeting Sheet.md", "Todo.md"}

    def __init__(
        self, force_graph_json_path: str, obsidian_directory_path: str
    ) -> None:
        self._force_graph_json_path = force_graph_json_path
        self._obsidian_directory_path = obsidian_directory_path

    def update_force_graph_json(self) -> None:
        """
        Updates the force graph JSON file with the current state of the Obsidian
        """

        def add_to_force_graph(force_graph: Dict[str, list], file_data, index=0):
            if isinstance(file_data, dict):
                file_data = file_data.items()

            for full_path, file_name in file_data:  # pylint: disable=unused-variable
                current_object = {"id": file_name, "name": file_name, "val": index}

                force_graph["nodes"].append(current_object)
                index += 1

            return index

        self._pull_repository_updates()

        if self._has_directory_changed():
            print("Changes detected, updating force graph")
        else:
            print("No changes to force graph")
            return

        file_data: GetAllFilesResult = self._get_all_files(
            self._obsidian_directory_path
        )
        markdown_files: Dict[str, str] = file_data["md_files"]
        other_files: Set[Tuple[str, str]] = file_data["other_files"]

        graph: List[Dict[str, str]] = []

        for path, file_name in markdown_files.items():
            links: Set[str] = self._extract_links_from_file(path, markdown_files)

            for connection_to in links:
                graph.append({"source": file_name, "target": connection_to})

        force_graph_data: Dict[str, list] = {"nodes": [], "links": []}

        index: int = add_to_force_graph(force_graph_data, markdown_files)
        add_to_force_graph(force_graph_data, other_files, index)

        for data in graph:
            force_graph_data["links"].append(data)

        with open(self._force_graph_json_path + ".json", "w", encoding="utf-8") as output_file:
            dump(force_graph_data, output_file)

    # PRIVATE METHODS START HERE

    def _get_all_files(
        self,
        path: str,
        md_files: Dict[str, str] | None = None,
        other_files: Set[Tuple[str, str]] | None = None,
    ) -> GetAllFilesResult:
        """
        Recursively scans a directory for Markdown files and other files.

        Args:
            md_files: A dictionary to store the found Markdown files, where the key is the
            file path and the value is the file name without the extension.
            other_files: A set to store other files found, where each entry is a tuple containing
            the file path and the file name.
        """

        if not md_files and not other_files:
            md_files = {}
            other_files = set()

        assert not md_files is None
        assert not other_files is None

        for file_name in listdir(path):
            if file_name in self.files_to_ignore or file_name in self.folders_to_ignore:
                continue

            current_path: str = f"{path}/{file_name}"

            if isdir(current_path):
                self._get_all_files(current_path, md_files, other_files)
            elif current_path.endswith(".md"):
                md_files[current_path] = file_name[: len(file_name) - 3]
            else:
                # TODO: remove .png, change this later to remove any extension
                other_files.add((current_path, file_name))

        return {"md_files": md_files, "other_files": other_files}

    # def get_file_force_graph_data(self, file_name: str, last_index)

    def _extract_links_from_file(
        self, path_to_file: str, md_files: Dict[str, str]
    ) -> Set[str]:
        """
        Extracts links from a Markdown file. The markdown file is assumed to follow the
        obsidian markdown structure.

        Args:
            path_to_file: The path to the Markdown file.

        Returns:
            A set of extracted links.
        """

        links: Set[str] = set()

        with open(path_to_file, "r", encoding="UTF-8") as md_file:
            for line in md_file:
                matches: List[str] = findall(r"\[\[(.*?)\]\]", line)

                for match in matches:
                    actual_link: str = ""
                    previous_character: str = ""

                    for character in match:
                        # "Ghaz's Notes#Table Of Contents | Contents" -> "Ghaz's Notes"
                        if (
                            previous_character != "\\"
                            and character == "#"
                            or character == "|"
                        ):
                            break

                        actual_link += character
                        previous_character = character

                    actual_link = actual_link.strip()
                    # TODO: LOOK FOR A BETTER SOLUTION

                    markdown_exists: bool = False

                    for file_name in md_files.values():
                        if file_name == actual_link:
                            markdown_exists = True
                            break

                    if markdown_exists:
                        links.add(actual_link)

        return links

    def _pull_repository_updates(self) -> None:
        """Pulls the latest updates from the Git repository."""
        try:
            run(["git", "-C", self._obsidian_directory_path, "pull"], check=True)
        except CalledProcessError as e:
            print(f"Failed to pull updates from repository: {e}")

    def _get_latest_modification_time(self, directory_path) -> float:
        latest_mod_time: float = 0

        for root, dirs, files in walk(directory_path):
            # Skip the .git directory
            if ".git" in dirs:
                dirs.remove(".git")

            for file in files:
                file_path = join(root, file)

                mod_time: float = getmtime(file_path)
                if mod_time > latest_mod_time:
                    latest_mod_time = mod_time

        return latest_mod_time

    def _get_last_update_timestamp(self) -> float:
        force_graph_json_directory_path = join(
            dirname(abspath(__file__)), "vault_update_timestamps.json"
        )

        if not exists(force_graph_json_directory_path):
            return 0

        with open(
            force_graph_json_directory_path,
            "r",
            encoding="UTF-8",
        ) as file:
            try:
                data = load(file)
                if self._force_graph_json_path in data:
                    return data[self._force_graph_json_path]
            except JSONDecodeError as e:
                print(
                    "Error occured while trying to load file, improper json deleting", e
                )
                remove(force_graph_json_directory_path)

        return 0

    def _has_directory_changed(self) -> bool:
        latest_mod_time = self._get_latest_modification_time(
            self._obsidian_directory_path
        )
        last_update_timestamp: float = self._get_last_update_timestamp()

        if latest_mod_time > last_update_timestamp:
            self._update_timestamp_in_json(latest_mod_time)
            return True

        return False

    def _update_timestamp_in_json(self, timestamp: float) -> bool:
        force_graph_json_directory_path = join(
            dirname(abspath(__file__)), "vault_update_timestamps.json"
        )

        time_stamp_json = {}

        if not exists(force_graph_json_directory_path):
            with open(
                force_graph_json_directory_path,
                "w",
                encoding="UTF-8",
            ) as file:
                dump({}, file)
        else:
            with open(
                force_graph_json_directory_path,
                "r",
                encoding="UTF-8",
            ) as file:
                time_stamp_json = load(file)
                time_stamp_json[self._force_graph_json_path] = timestamp

        with open(
            force_graph_json_directory_path,
            "w",
            encoding="UTF-8",
        ) as file:
            dump(time_stamp_json, file)

        return True
