import os
import time
import requests
from typing import Dict, Iterable
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

HUBSPOT_BASE = "https://api.hubapi.com"

class HubSpotAuthError(Exception):
    pass

class HubSpotRateLimit(Exception):
    pass

def _headers():
    token = os.getenv("HUBSPOT_TOKEN")
    if not token:
        raise HubSpotAuthError("HUBSPOT_TOKEN not set. Create a Private App token and set it in your environment.")
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

@retry(
    wait=wait_exponential(multiplier=1, min=2, max=60),
    stop=stop_after_attempt(5),
    reraise=True,
    retry=retry_if_exception_type((HubSpotRateLimit, requests.RequestException)),
)
def get_paginated(endpoint: str, params: Dict) -> Iterable[Dict]:
    url = f"{HUBSPOT_BASE}{endpoint}"
    params = dict(params)
    params.setdefault("limit", 100)
    after = None

    while True:
        if after:
            params["after"] = after

        resp = requests.get(url, headers=_headers(), params=params, timeout=60)
        if resp.status_code == 429:
            retry_after = int(resp.headers.get("Retry-After", "2"))
            time.sleep(retry_after)
            raise HubSpotRateLimit("429 Too Many Requests")

        resp.raise_for_status()
        data = resp.json()
        for item in data.get("results", []):
            yield item

        next_after = data.get("paging", {}).get("next", {}).get("after")
        if not next_after:
            break
        after = next_after
