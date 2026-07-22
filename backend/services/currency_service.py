from datetime import date

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

import models.currency as currency
import services.mocks.currency_rates_mock as currency_rates_dev
from core.config import settings
from db.models import CurrencyRate
from services.providers.frankfurter_client import FrankfurterClient

client = FrankfurterClient()


def get_currency_rates(base_currency, db: Session):
    base_c = base_currency.upper()
    if settings.MOCK_DATA:
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

    rates_map = _load_or_fetch_eur_rates(db)
    currency_rates = [
        currency.CurrencyRate(
            exchange_currency=c,
            rate=r,
        )
        for c, r in convert_base(base_c, rates_map).items()
    ]
    return currency.RateResponse(
        base_currency=base_c,
        rates=currency_rates,
    )


def _load_or_fetch_eur_rates(db: Session) -> dict[str, float]:
    today = date.today()
    rows = db.scalars(
        select(CurrencyRate).where(
            CurrencyRate.fetch_date == today,
            CurrencyRate.base_currency == "EUR",
        )
    ).all()

    if rows:
        return {r.target_currency: r.rate for r in rows}

    rates_data = client.get_exchange_rate()
    rates = rates_data["rates"]
    rates["EUR"] = 1

    stmt = (
        insert(CurrencyRate)
        .values(
            [
                {
                    "fetch_date": today,
                    "base_currency": "EUR",
                    "target_currency": c,
                    "rate": r,
                }
                for c, r in rates.items()
            ]
        )
        .on_conflict_do_nothing(
            index_elements=["fetch_date", "base_currency", "target_currency"]
        )
    )
    db.execute(stmt)
    db.commit()
    return rates


def convert_base(base_currency, rates):
    try:
        base_rate = rates[base_currency]
    except KeyError:
        raise KeyError(f"Unknown currency: {base_currency}")

    new_rates = {}
    for c, rate in rates.items():
        new_rates[c] = rate / base_rate

    return new_rates
