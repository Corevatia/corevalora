from datetime import UTC, date, datetime, timedelta

import pytest

from core.config import settings
from core.errors import AssetNotFound, ProviderRejected, UpstreamUnavailable
from db.models import AssetPriceCache
from services import stock_service
from services.cache.price_cache import CACHE_TTL_SECONDS
from services.cache.search_cache import read_search
from services.exchanges import figi_filter


class FakeClient:
    def __init__(self, eod_error, backup_error=None):
        self.eod_error = eod_error
        self.backup_error = backup_error
        self.backup_calls = 0

    def get_asset_eod(self, symbol):
        raise self.eod_error

    def get_asset_price_backup(self, symbol):
        self.backup_calls += 1
        if self.backup_error:
            raise self.backup_error
        return {
            "data": [
                {
                    "symbol": symbol,
                    "close": "150.25",
                    "exchange": "XNAS",
                    "date": "2026-07-15T00:00:00+0000",
                }
            ]
        }

    def search_tickers_backup(self, symbol):
        return {"data": [{"name": "Apple Inc"}]}


class FakeSearchClient:
    def __init__(self, symbols):
        self.symbols = symbols

    def _items(self, ticker_field):
        return {
            "data": [
                {
                    ticker_field: s,
                    "name": s,
                    "has_eod": True,
                    "stock_exchange": {"name": "SIX Swiss Exchange", "mic": "XSWX"},
                }
                for s in self.symbols
            ]
        }

    def search_tickers(self, query):
        return self._items("ticker")

    def search_tickers_backup(self, query):
        return self._items("symbol")


class FakeFigiClient:
    def __init__(self, answers=None, error=None):
        self.answers = answers
        self.error = error

    def map_tickers(self, jobs):
        if self.error:
            raise self.error
        return self.answers


FIGI_KNOWN = {"data": [{"figi": "BBG000TEST00"}]}
FIGI_UNKNOWN = {"warning": "No identifier found."}


@pytest.fixture
def search_setup(monkeypatch):
    monkeypatch.setattr(settings, "MOCK_DATA", False)
    monkeypatch.setattr(settings, "OPENFIGI_FILTER", "silent")
    monkeypatch.setattr(
        stock_service, "client", FakeSearchClient(["NESN.SW", "NESNE.SW"])
    )

    def use_figi(fake):
        monkeypatch.setattr(figi_filter, "client", fake)

    return use_figi


@pytest.mark.parametrize(
    "search, kind",
    [
        (stock_service.get_stock_search, "stock"),
        (stock_service.search_backup, "bstock"),
    ],
)
def test_search_marks_unknown_tickers_and_caches(db, search_setup, search, kind):
    search_setup(FakeFigiClient([FIGI_KNOWN, FIGI_UNKNOWN]))

    results = search("nestle", db)

    assert [(r.symbol, r.verified) for r in results] == [
        ("NESN.SW", True),
        ("NESNE.SW", False),
    ]
    cached = read_search(db, kind=kind, query="nestle")
    assert [(r["symbol"], r["verified"]) for r in cached.results] == [
        ("NESN.SW", True),
        ("NESNE.SW", False),
    ]


def test_search_without_openfigi_is_unmarked_and_not_cached(db, search_setup):
    search_setup(FakeFigiClient(error=UpstreamUnavailable("/v3/mapping -> 503")))

    results = stock_service.get_stock_search("nestle", db)

    assert [(r.symbol, r.verified) for r in results] == [
        ("NESN.SW", None),
        ("NESNE.SW", None),
    ]
    assert read_search(db, kind="stock", query="nestle") is None


def stale_cache_row():
    return AssetPriceCache(
        kind="stock",
        key="AAPL",
        symbol="AAPL",
        asset_name="Apple Inc",
        price=100.0,
        currency="USD",
        exchange="XNAS",
        price_date=date(2026, 7, 1),
        cached_at=datetime.now(UTC)
        - timedelta(seconds=CACHE_TTL_SECONDS["stock"] + 60),
    )


def test_upstream_error_without_cache_does_not_fall_back_to_v1(db, monkeypatch):
    fake = FakeClient(UpstreamUnavailable("/v2/eod -> 429"))
    monkeypatch.setattr(settings, "MOCK_DATA", False)
    monkeypatch.setattr(stock_service, "client", fake)

    with pytest.raises(UpstreamUnavailable):
        stock_service.get_price("AAPL", db)

    assert fake.backup_calls == 0


def test_unsupported_symbol_falls_back_to_v1(db, monkeypatch):
    fake = FakeClient(ProviderRejected("/v2/eod -> 422"))
    monkeypatch.setattr(settings, "MOCK_DATA", False)
    monkeypatch.setattr(stock_service, "client", fake)

    result = stock_service.get_price("AAPL", db)

    assert fake.backup_calls == 1
    assert result.price == 150.25
    assert result.currency == "USD"
    assert result.stale is False


def test_symbol_rejected_by_both_versions_is_not_found(db, monkeypatch):
    fake = FakeClient(
        ProviderRejected("/v2/eod -> 422"),
        backup_error=ProviderRejected("/v1/eod -> 422"),
    )
    monkeypatch.setattr(settings, "MOCK_DATA", False)
    monkeypatch.setattr(stock_service, "client", fake)

    with pytest.raises(AssetNotFound):
        stock_service.get_price("NOPE", db)

    assert fake.backup_calls == 1


def test_unknown_symbol_never_serves_stale_cache(db, monkeypatch):
    db.add(stale_cache_row())
    db.flush()
    fake = FakeClient(AssetNotFound("/v2/eod -> 404"))
    monkeypatch.setattr(settings, "MOCK_DATA", False)
    monkeypatch.setattr(stock_service, "client", fake)

    with pytest.raises(AssetNotFound):
        stock_service.get_price("AAPL", db)


def test_upstream_error_with_cache_serves_stale(db, monkeypatch):
    db.add(stale_cache_row())
    db.flush()
    fake = FakeClient(UpstreamUnavailable("/v2/eod -> 500"))
    monkeypatch.setattr(settings, "MOCK_DATA", False)
    monkeypatch.setattr(stock_service, "client", fake)

    result = stock_service.get_price("AAPL", db)

    assert fake.backup_calls == 0
    assert result.price == 100.0
    assert result.stale is True
