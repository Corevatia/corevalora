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

    # Portugal
    "XLIS": "EUR",

    # UK
    "XLON": "GBP",

    # Canada
    "XTSE": "CAD",
    "XCNQ": "CAD",

    # Australia
    "XASX": "AUD",

    # Japan
    "XNGO": "JPY",
    "XFKA": "JPY",
    "XSAP": "JPY",

    # China
    "XSHG": "CNY",
    "XSHE": "CNY",

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

    # Taiwan
    "XTAI": "TWD",

    # Turkey
    "XIST": "TRY",

    # New Zealand
    "XNZE": "NZD",

    # Qatar
    "DSMD": "QAR",

    # Saudi
    "XSAU": "SAR",
}


def get_exchange_currency(mic):
    currency = EXCHANGE_CURRENCY.get(mic)
    if not currency:
        print(f"[WARN] Unknown exchange MIC: {mic}")
    return currency
