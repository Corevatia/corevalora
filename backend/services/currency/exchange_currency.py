import logging

logger = logging.getLogger(__name__)

EXCHANGE_CURRENCY = {

    # USA
    "XNAS": "USD",  # NASDAQ
    "XNYS": "USD",  # NYSE
    "XASE": "USD",  # NYSE American
    "ARCX": "USD",  # NYSE Arca
    "IEXG": "USD",  # IEX

    # Switzerland
    "XSWX": "CHF",  # SIX Swiss Exchange

    # Germany
    "XETRA": "EUR",  # Xetra
    "XETR": "EUR",  # Xetra
    "XFRA": "EUR",  # Frankfurt
    "XSTU": "EUR",  # Stuttgart

    # France
    "XPAR": "EUR",

    # Netherlands
    "XAMS": "EUR",

    # Belgium
    "XBRU": "EUR",

    # Italy
    "XMIL": "EUR",

    # Spain
    "BMEX": "EUR",
    "XMAD": "EUR",

    # Portugal
    "XLIS": "EUR",

    # UK
    "XLON": "GBP",

    # Canada
    "XTSE": "CAD",
    "XCNQ": "CAD",

    # Japan
    "XSAP": "JPY",
    "XJPX": "JPY",
    "XFKA": "JPY",
    "XNGO": "JPY",

    # Hong Kong
    "XHKG": "HKD",

    # Singapore
    "XSES": "SGD",

    # Korea
    "XKRX": "KRW",

    # India
    "XBOM": "INR",
    "XNSE": "INR",

    # Sweden
    "XSTO": "SEK",

    # Denmark
    "XCSE": "DKK",

    # Norway
    "XOSL": "NOK",

    # Poland
    "XWAR": "PLN",

    # Israel
    "XTAE": "ILS",

    # Mexico
    "XMEX": "MXN",

    # South Africa
    "XJSE": "ZAR",

    # Thailand
    "XBKK": "THB",

    # New Zealand
    "XNZE": "NZD",
}


def get_exchange_currency(mic):
    currency = EXCHANGE_CURRENCY.get(mic)
    if not currency:
        logger.error(f"Exchange not supported{mic}")
    return currency
