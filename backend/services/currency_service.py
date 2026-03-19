import dotenv
import requests

from services.providers.frankfurter_client import FrankfurterClient
import os
import models.currency as currency
import services.currency.currency_rates_dev as currency_rates_dev

dotenv.load_dotenv()
client = FrankfurterClient()


def get_currency_rates(base_currency):
    base_c = base_currency.upper()
    if os.getenv("DEV_MODE") == "true":

        dev_rates = [
            currency.CurrencyRate(
                exchange_currency=c,
                rate=rate,
                )
            for c, rate in convert_base(base_c, currency_rates_dev.RATES).items()
            ]
        return currency.RateResponse(
            base_currency=base_c,
            rates=dev_rates,
        )

    rates_data = client.get_exchange_rate()
    rates = rates_data["rates"]
    rates["EUR"] = 1
    currency_rates = [
        currency.CurrencyRate(
            exchange_currency=c,
            rate=rate,
        )
        for c, rate in convert_base(base_c, rates_data["rates"]).items()
    ]
    return currency.RateResponse(
        base_currency=base_c,
        rates=currency_rates,
    )


def convert_base(base_currency, rates):
    try:
        base_rate = rates[base_currency]
    except KeyError:
        raise ValueError(404, f"can't get currency rate for {base_currency}")

    new_rates = {}
    for c, rate in rates.items():
        new_rates[c] = rate / base_rate

    return new_rates

