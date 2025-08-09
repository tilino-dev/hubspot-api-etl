from typing import Dict, List
import yaml
from .hubspot_client import get_paginated
from .utils import window_from_env

def extract_objects(config_path: str = "configs/objects.yml") -> Dict[str, List[dict]]:
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    start, end = window_from_env()
    _ = (start, end)
    out: Dict[str, List[dict]] = {}
    for obj in cfg["objects"]:
        name = obj["name"]
        endpoint = obj["endpoint"]
        props = obj["properties"]
        params = {"properties": ",".join(props), "archived": False}
        rows: List[dict] = []
        for rec in get_paginated(endpoint, params):
            rows.append(rec)
        out[name] = rows
    return out

if __name__ == "__main__":
    data = extract_objects()
    for k, v in data.items():
        print(k, len(v))
