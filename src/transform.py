from __future__ import annotations
from typing import Dict, List
import pandas as pd

def _flatten(records: List[dict]) -> pd.DataFrame:
    if not records:
        return pd.DataFrame()
    props = [r.get("properties", {}) for r in records]
    ids = [int(r.get("id")) for r in records]
    df = pd.DataFrame(props)
    df.insert(0, "hs_object_id", ids)
    for col in df.columns:
        if col.endswith("date") or col.endswith("datetime") or ("date" in col and col.startswith("hs_")):
            try:
                df[col] = pd.to_datetime(df[col], utc=True, errors="coerce")
            except Exception:
                pass
    return df

def transform(extracted: Dict[str, List[dict]]) -> Dict[str, pd.DataFrame]:
    return {name: _flatten(recs) for name, recs in extracted.items()}
