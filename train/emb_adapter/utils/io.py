import json
from typing import Any, List, Dict

def read_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def write_json(obj: Any, path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

# Expected schema for train/val: list of {"question": str, "chunk": str}
def validate_supervision_schema(records: List[Dict[str, str]]) -> None:
    required = {"question", "chunk"}
    for i, r in enumerate(records):
        if not required.issubset(r):
            raise ValueError(f"Row {i} missing keys {required - set(r)}")
