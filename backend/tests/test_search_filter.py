from services.search_filter import filter_marketstack_search


def _item(mic, has_eod=True):
    return {
        "symbol": "AAPL",
        "has_eod": has_eod,
        "stock_exchange": {"mic": mic},
    }


def test_keeps_supported_exchange():
    result = filter_marketstack_search({"data": [_item("XNAS")]})
    assert len(result) == 1
    assert result[0]["stock_exchange"]["mic"] == "XNAS"


def test_drops_unsupported_exchange():
    result = filter_marketstack_search({"data": [_item("ZZZZ")]})
    assert result == []


def test_drops_item_without_eod():
    result = filter_marketstack_search({"data": [_item("XNAS", has_eod=False)]})
    assert result == []


def test_handles_missing_data_key():
    assert filter_marketstack_search({}) == []


def test_handles_empty_data():
    assert filter_marketstack_search({"data": []}) == []