import logging

import pytest

from core.errors import AssetNotFound, UpstreamUnavailable
from models.stock import SearchResult
from services.exchanges import figi_filter
from services.exchanges.figi_filter import (
    build_figi_job,
    mark_with_figi,
    normalize_for_figi,
)
from services.providers.openfigi_client import OpenFigiClient

KNOWN = {"data": [{"figi": "BBG000TEST00"}]}
UNKNOWN = {"warning": "No identifier found."}


class FakeFigiClient:
    def __init__(self, answers=None, error=None):
        self.answers = answers
        self.error = error
        self.jobs = None

    def map_tickers(self, jobs):
        self.jobs = jobs
        if self.error:
            raise self.error
        return self.answers


def _result(symbol, mic):
    return SearchResult(key=symbol, name=symbol, symbol=symbol, exchange="", mic=mic)


@pytest.mark.parametrize(
    "ticker, mic, expected",
    [
        ("SAP.DE", "XETR", ("SAP", "XETR")),
        ("NESN.SW", "XSWX", ("NESN", "XSWX")),
        ("NOVO-B.CO", "XCSE", ("NOVOB", "XCSE")),
        ("BRK-B", "XNYS", ("BRK/B", "XNYS")),
        ("AAPL", "XNAS", ("AAPL", "XNAS")),
        ("0700.HK", "XHKG", ("700", "XHKG")),
        ("7203.T", "XJPX", ("7203", "XTKS")),
    ],
)
def test_normalize_for_figi(ticker, mic, expected):
    assert normalize_for_figi(ticker, mic) == expected


def test_job_uses_mic_code():
    assert build_figi_job("NESN", "XSWX") == {
        "idType": "TICKER",
        "idValue": "NESN",
        "micCode": "XSWX",
    }


def test_nasdaq_job_uses_us_exchange_code():
    assert build_figi_job("AAPL", "XNAS") == {
        "idType": "TICKER",
        "idValue": "AAPL",
        "exchCode": "US",
    }


def test_sends_normalized_jobs(monkeypatch):
    fake = FakeFigiClient(answers=[KNOWN])
    monkeypatch.setattr(figi_filter, "client", fake)

    mark_with_figi([_result("NOVO-B.CO", "XCSE")], "silent")

    assert fake.jobs == [{"idType": "TICKER", "idValue": "NOVOB", "micCode": "XCSE"}]


def test_off_does_not_call_openfigi(monkeypatch):
    fake = FakeFigiClient(answers=[UNKNOWN])
    monkeypatch.setattr(figi_filter, "client", fake)
    results = [_result("NESNE.SW", "XSWX")]

    marked, cacheable = mark_with_figi(results, "off")

    assert [r.verified for r in marked] == [None]
    assert cacheable is True
    assert fake.jobs is None


@pytest.mark.parametrize("mode, logged", [("silent", False), ("verbose", True)])
def test_marks_known_and_unknown(monkeypatch, caplog, mode, logged):
    caplog.set_level(logging.INFO, logger=figi_filter.__name__)
    rejected = {"error": "Invalid micCode."}
    fake = FakeFigiClient([KNOWN, UNKNOWN, rejected])
    monkeypatch.setattr(figi_filter, "client", fake)
    results = [
        _result("NESN.SW", "XSWX"),
        _result("NESNE.SW", "XSWX"),
        _result("SAP.DE", "XETR"),
    ]

    marked, cacheable = mark_with_figi(results, mode)

    assert [r.symbol for r in marked] == ["NESN.SW", "NESNE.SW", "SAP.DE"]
    assert [r.verified for r in marked] == [True, False, None]
    assert cacheable is True
    assert ("NESNE.SW" in caplog.text) is logged


def test_preferred_share_is_not_checked(monkeypatch):
    fake = FakeFigiClient(answers=[UNKNOWN])
    monkeypatch.setattr(figi_filter, "client", fake)
    results = [_result("BAC-P-L", "XNYS"), _result("NESNE.SW", "XSWX")]

    marked, _ = mark_with_figi(results, "silent")

    assert len(fake.jobs) == 1
    assert [r.verified for r in marked] == [None, False]


@pytest.mark.parametrize(
    "error",
    [UpstreamUnavailable("/v3/mapping -> 429"), AssetNotFound("/v3/mapping -> 404")],
)
def test_openfigi_failure_is_unmarked_and_not_cacheable(monkeypatch, error):
    monkeypatch.setattr(figi_filter, "client", FakeFigiClient(error=error))
    results = [_result("NESNE.SW", "XSWX")]

    marked, cacheable = mark_with_figi(results, "verbose")

    assert [r.verified for r in marked] == [None]
    assert cacheable is False


def test_answer_count_mismatch_is_not_cacheable(monkeypatch):
    monkeypatch.setattr(figi_filter, "client", FakeFigiClient([KNOWN]))
    results = [_result("NESN.SW", "XSWX"), _result("NESNE.SW", "XSWX")]

    marked, cacheable = mark_with_figi(results, "silent")

    assert [r.verified for r in marked] == [None, None]
    assert cacheable is False


@pytest.mark.parametrize("api_key, request_sizes", [(None, [10, 10, 5]), ("key", [25])])
def test_client_splits_jobs_into_chunks(monkeypatch, api_key, request_sizes):
    client = OpenFigiClient(api_key=api_key)
    sizes = []

    def fake_post(url, payload):
        sizes.append(len(payload))
        return [KNOWN] * len(payload)

    monkeypatch.setattr(client, "_post", fake_post)

    results = client.map_tickers([{"idValue": str(i)} for i in range(25)])

    assert sizes == request_sizes
    assert len(results) == 25
