import json
from pathlib import Path

DATA_DIR = Path(__file__).parent
INVENTORY_PATH = DATA_DIR / "inventory.json"
ORDERS_PATH = DATA_DIR / "orders.json"


def load_data(json_path: Path):
    if json_path.exists():
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return []


def save_data(file_list: list, json_path: Path):
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(file_list, f, indent=4)