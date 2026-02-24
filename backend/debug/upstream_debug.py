import dotenv
import os

dotenv.load_dotenv()


def upstream_debug(r):
    UPSTREAM_DEBUG = os.getenv("UPSTREAM_DEBUG", "false").lower() == "true"

    if UPSTREAM_DEBUG:
        print("Upstream status:", r.status_code)
        print("Upstream body:", r.text[:300])

    try:
        r.raise_for_status()
    except Exception as e:
        print("HTTP ERROR:", e)
        print("Status:", r.status_code)
        print("Body:", r.text)
