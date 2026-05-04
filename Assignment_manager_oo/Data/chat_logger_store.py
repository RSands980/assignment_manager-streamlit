import json
from pathlib import Path


class ChatLoggerStore:
    def __init__(self, json_path: Path) -> None:
        self.__json_path = json_path

    def load_logs(self) -> list:
        if self.__json_path.exists():
            with open(self.__json_path, "r") as file:
                return json.load(file)
        return []

    def save_logs(self, logs: list) -> None:
        with open(self.__json_path, "w") as file:
            json.dump(logs, file, indent=2)