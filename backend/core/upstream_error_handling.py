import dotenv
import os
import requests

dotenv.load_dotenv()


def upstream_error_handling(r: requests.Response):
    upstream_debug = os.getenv("UPSTREAM_DEBUG", "false").lower() == "true"

    if upstream_debug:
        print("Upstream status:", r.status_code)
        print("Upstream body:", r.text[:300])

    try:
        r.raise_for_status()
    except requests.HTTPError as e:
        print("HTTP ERROR:", e)
        print("Status:", r.status_code)
        print("Body:", r.text[:300])
        raise
