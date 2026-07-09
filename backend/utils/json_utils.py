import json
import os
from typing import Any, List

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def _get_path(filename: str) -> str:
    return os.path.join(DATA_DIR, filename)


def read_json(filename: str) -> List[dict]:
    path = _get_path(filename)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def write_json(filename: str, data: List[dict]) -> None:
    path = _get_path(filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def next_id(data: List[dict]) -> int:
    if not data:
        return 1
    return max(item["id"] for item in data) + 1
