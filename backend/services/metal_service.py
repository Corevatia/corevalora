import logging

from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy.orm import Session

from core.config import settings
from core.errors import AssetNotFound, UpstreamError
from models import metal
from models.metal import SupportedMetal
from services.cache.price_cache import is_fresh, read_price, upsert_price
from services.mocks.metal_mock import get_metal_mock
from services.providers.metalsdev_client import MetalsDevClient

logger = logging.getLogger(__name__)

client = MetalsDevClient(api_key=settings.METALS_DEV_API_KEY)


SUPPORTED_METALS = {
    "gold": SupportedMetal(key="gold", name="Gold", symbol="Au"),
    "silver": SupportedMetal(key="silver", name="Silver", symbol="Ag"),
    "platinum": SupportedMetal(key="platinum", name="Platinum", symbol="Pt"),
    "palladium": SupportedMetal(key="palladium", name="Palladium", symbol="Pd"),
}


def get_metal(key: str) -> SupportedMetal:
    try:
        return SUPPORTED_METALS[key]
    except KeyError:
        raise AssetNotFound(f"unknown metal {key}") from None


def get_supported_metals() -> list[SupportedMetal]:
    return list(SUPPORTED_METALS.values())


def get_price(key: str, db: Session) -> metal.Metal:
    requested = get_metal(key)

    if settings.MOCK_DATA:
        return get_metal_mock()

    cached = read_price(db, kind="metal", key=key)

    if cached and is_fresh(cached, "metal"):
        return _cache_to_metal(cached, stale=False)

    try:
        data = client.get_latest_metals()
        currency = data["currency"]
        price_date = data["timestamps"]["metal"][:10]

        for metal_key, supported in SUPPORTED_METALS.items():
            upsert_price(
                db,
                kind="metal",
                key=metal_key,
                symbol=supported.symbol,
                asset_name=supported.name,
                price=float(data["metals"][metal_key]),
                currency=currency,
                price_date=price_date,
            )

        return metal.Metal(
            key=key,
            symbol=requested.symbol,
            name=requested.name,
            price=float(data["metals"][key]),
            currency=currency,
            date=price_date,
            stale=False,
        )
    except (UpstreamError, IntegrityError, DataError) as e:
        if cached:
            logger.warning(f"Could not refresh metal {key} serving stale: {e}")
            return _cache_to_metal(cached, stale=True)
        raise


def _cache_to_metal(cached, stale: bool) -> metal.Metal:
    return metal.Metal(
        key=cached.key,
        symbol=cached.symbol,
        name=cached.asset_name,
        price=cached.price,
        currency=cached.currency,
        date=cached.price_date.strftime("%Y-%m-%d"),
        stale=stale,
    )
