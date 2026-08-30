from models import metal


def get_metal_mock():
    return metal.Metal(
        key="gold",
        symbol="Au",
        name="Gold",
        price=130,
        currency="USD",
        date="2026-01-01",
        stale=False,
    )
