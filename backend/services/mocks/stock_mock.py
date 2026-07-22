import models.stock as stock


def get_stock_mock() -> stock.Stock:
    return stock.Stock(
        symbol="STXY",
        key="key",
        price=123.45,
        date="2026-02-23",
        exchange="exch",
        name="StockXY",
        currency="CHF",
        stale=False,
    )


def get_stock_search_results_mock():
    return [
        stock.SearchResult(
            key="STXY", name="StockXY", symbol="STXY", exchange="EXCHANGE", mic="EXCH"
        ),
        stock.SearchResult(
            key="STYX", name="StockYX", symbol="STYX", exchange="EXCHANGE", mic="STYX"
        ),
    ]
