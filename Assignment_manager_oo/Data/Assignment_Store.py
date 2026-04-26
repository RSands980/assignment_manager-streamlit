import json
from pathlib import Path


class AssignmentStore:
    def __init__(self, json_path: Path) -> None:
        self._json_path = json_path

    def load(self) -> list[dict]:
        if self._json_path.exists():
            with open(self._json_path, "r") as file:
                return json.load(file)
        return []

    def save(self, assignments: list[dict]) -> None:
        with open(self._json_path, "w") as file:
            json.dump(assignments, file, indent=2)