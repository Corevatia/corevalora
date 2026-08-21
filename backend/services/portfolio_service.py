import logging
from collections.abc import Iterable
from datetime import date
from math import inf

from sqlalchemy import select
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy.orm import Session, selectinload

from core.errors import (
    CoreValoraError,
    HoldingNotFound,
    InsufficientHoldingAmount,
    TransactionNotFound,
)
from db.models import Holding, Transaction, User
from models.portfolio import HoldingIn, HoldingOut, TransactionIn, TransactionOut
from services import crypto_service, stock_service

logger = logging.getLogger(__name__)


AMOUNT_EPSILON = 1e-9


def compute_avg_price(
    old_amount: float, old_avg: float, add_amount: float, add_price: float
) -> tuple[float, float]:
    new_amount = old_amount + add_amount
    new_avg = (old_amount * old_avg + add_amount * add_price) / new_amount
    return new_amount, new_avg


def aggregate_transactions(
    transactions: Iterable[Transaction],
) -> tuple[float, float]:
    amount = 0.0
    avg_price = 0.0

    for tx in transactions:
        if tx.side == "buy":
            amount, avg_price = compute_avg_price(
                amount, avg_price, tx.amount, tx.price
            )
        else:
            amount -= tx.amount

    return amount, avg_price


def check_coverage(transactions: Iterable[Transaction], key: str) -> None:
    amount = 0.0

    for tx in transactions:
        amount += tx.amount if tx.side == "buy" else -tx.amount
        if amount < -AMOUNT_EPSILON:
            raise InsufficientHoldingAmount(
                f"{key}: {tx.side} of  {tx.amount} on {tx.traded_on}"
                f"would leave {amount}"
            )


def list_holdings(user: User, db: Session) -> list[HoldingOut]:
    holdings = (
        db.execute(
            select(Holding)
            .where(Holding.user_id == user.id)
            .options(selectinload(Holding.transactions))
        )
        .scalars()
        .all()
    )
    priced = []
    for holding in holdings:
        amount, avg_price = aggregate_transactions(holding.transactions)
        if amount <= AMOUNT_EPSILON:
            continue
        priced.append(_safe_enrich_holding(holding, db, amount, avg_price))

    return priced


def _safe_enrich_holding(
    holding: Holding, db: Session, amount: float, avg_price: float
) -> HoldingOut:
    try:
        return _enrich_holding(holding, db, amount, avg_price)
    except (CoreValoraError, IntegrityError, DataError) as e:
        logger.warning(
            "Failed to price holding id=%s key=%s; returning degraded entry: %s",
            holding.id,
            holding.key,
            e,
        )
        return HoldingOut(
            id=holding.id,
            asset=holding.asset,
            key=holding.key,
            symbol=holding.symbol,
            kind=holding.kind,
            amount=amount,
            avg_price=avg_price,
            price=None,
            currency=None,
            exchange=None,
            price_date=None,
            stale=True,
        )


def add_transaction(data: TransactionIn, user: User, db: Session) -> HoldingOut:
    holding = _find_position(data, user, db)
    transaction = Transaction(
        side=data.side,
        amount=data.amount,
        price=data.price,
        traded_on=data.traded_on,
    )

    if data.side == "sell":
        held = holding.transactions if holding is not None else []
        check_coverage(_in_trade_order(held, transaction), data.key)

    if holding is None:
        holding = Holding(
            key=data.key,
            user_id=user.id,
            asset=data.asset,
            symbol=data.symbol,
            kind=data.kind,
        )
        db.add(holding)

    holding.transactions.append(transaction)

    db.commit()
    db.refresh(holding)

    amount, avg_price = aggregate_transactions(holding.transactions)
    return _enrich_holding(holding, db, amount, avg_price)


def add_holding(data: HoldingIn, user: User, db: Session) -> HoldingOut:
    # Temporary so frontend keeps working
    return add_transaction(
        TransactionIn(
            asset=data.asset,
            key=data.key,
            symbol=data.symbol,
            kind=data.kind,
            side="buy",
            amount=data.amount,
            price=data.buy_price,
            traded_on=date.today(),
        ),
        user,
        db,
    )


def _find_position(data: TransactionIn, user: User, db: Session) -> Holding | None:
    return db.execute(
        select(Holding).where(
            Holding.user_id == user.id,
            Holding.key == data.key,
            Holding.kind == data.kind,
        )
    ).scalar_one_or_none()


def _in_trade_order(
    stored: Iterable[Transaction], pending: Transaction
) -> list[Transaction]:

    return sorted(
        [*stored, pending],
        key=lambda tx: (tx.traded_on, inf if tx.id is None else tx.id),
    )


def list_transactions(holding_id: int, user: User, db: Session) -> list[TransactionOut]:
    holding = _get_own_holding(holding_id, user, db)

    return [TransactionOut.model_validate(tx) for tx in reversed(holding.transactions)]


def delete_transaction(transaction_id: int, user: User, db: Session) -> None:
    transaction = db.execute(
        select(Transaction)
        .join(Holding)
        .where(Transaction.id == transaction_id, Holding.user_id == user.id)
    ).scalar_one_or_none()

    if transaction is None:
        raise TransactionNotFound(f"id {transaction_id} for user {user.id}")

    holding = transaction.holding
    remaining = [tx for tx in holding.transactions if tx.id != transaction_id]
    check_coverage(remaining, holding.key)

    db.delete(transaction)
    db.commit()


def delete_holding(holding_id: int, user: User, db: Session) -> None:
    holding = _get_own_holding(holding_id, user, db)

    db.delete(holding)
    db.commit()


def _get_own_holding(holding_id: int, user: User, db: Session) -> Holding:
    holding = db.execute(
        select(Holding).where(
            Holding.id == holding_id,
            Holding.user_id == user.id,
        )
    ).scalar_one_or_none()

    if holding is None:
        raise HoldingNotFound(f"id {holding_id} for user {user.id}")

    return holding


def _enrich_holding(
    holding: Holding, db: Session, amount: float, avg_price: float
) -> HoldingOut:
    if holding.kind == "crypto":
        priced = crypto_service.get_crypto_price(holding.key, db)
        exchange = None
    else:
        priced = stock_service.get_price(holding.key, db)
        exchange = priced.exchange

    return HoldingOut(
        id=holding.id,
        asset=holding.asset,
        key=holding.key,
        symbol=holding.symbol,
        kind=holding.kind,
        amount=amount,
        avg_price=avg_price,
        price=priced.price,
        currency=priced.currency,
        exchange=exchange,
        price_date=priced.date,
        stale=priced.stale,
    )
