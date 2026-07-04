import models.crypto as crypto

def get_crypto_mock():
    return crypto.Crypto(
            key="key",
            symbol="XYC",
            name="XYCoin",
            price=123.45,
            currency="USD",
            date="2021-09-22",
            stale=False,
        )
def get_crypto_search_results_mock():
    return [crypto.SearchResult(key="kyc", symbol="KYC", name="KYCoin", rank=123),
            crypto.SearchResult(key="xyc", symbol="XYC", name="XYCoin", rank=1)]
