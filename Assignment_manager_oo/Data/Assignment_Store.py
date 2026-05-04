import json
from pathlib import Path


class AssignmentStore:
    def __init__(self, json_path: Path) -> None:
        self.__json_path = json_path

    def load(self) -> list[dict]:
        if self.__json_path.exists():
            with open(self.__json_path, "r") as file:
                return json.load(file)
        return []

    def save(self, assignments: list[dict]) -> None:
        with open(self.__json_path, "w") as file:
            json.dump(assignments, file, indent=2)

    def get_assignments_as_string(self) -> str:
        if not self.__json_path.exists():
            return "[]"

        with open(self.__json_path, "r") as file:
            data = json.load(file)
            return json.dumps(data, indent=2)