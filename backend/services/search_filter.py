from services.exchange_currency import EXCHANGE_CURRENCY

SUPPORTED_MICS = set(EXCHANGE_CURRENCY.keys())


def filter_marketstack_search(search_json: dict):
    data = search_json.get("data") or []

    filtered = [
        item
        for item in data
        if item.get("has_eod") is True
           and item.get("stock_exchange", {}).get("mic") in SUPPORTED_MICS
    ]

    return filtered
