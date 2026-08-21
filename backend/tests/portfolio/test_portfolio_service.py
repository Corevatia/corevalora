import pytest

from core.errors import InsufficientHoldingAmount
from db.models import Transaction
from services.portfolio_service import (
    aggregate_transactions,
    check_coverage,
    compute_avg_price,
)


def buy(amount, price):
    return Transaction(side="buy", amount=amount, price=price)


def sell(amount, price=0):
    return Transaction(side="sell", amount=amount, price=price)


def test_equal_amounts_average_in_the_middle():
    amount, avg = compute_avg_price(10, 100, 10, 200)
    assert amount == 20

    assert avg == 150


def test_weighted_by_amount():
    amount, avg = compute_avg_price(1, 100, 9, 200)
    assert amount == 10
    assert avg == 190


def test_same_price_keeps_average():
    amount, avg = compute_avg_price(5, 50, 5, 50)
    assert amount == 10
    assert avg == 50


def test_fractional_amounts():
    amount, avg = compute_avg_price(0.5, 100, 0.5, 300)
    assert amount == 1.0
    assert avg == 200


def test_position_without_transactions_is_empty():
    assert aggregate_transactions([]) == (0.0, 0.0)


def test_two_buys_are_weighted():
    amount, avg = aggregate_transactions([buy(10, 100), buy(10, 200)])
    assert amount == 20
    assert avg == 150


def test_sell_shrinks_amount_but_keeps_avg_price():
    amount, avg = aggregate_transactions([buy(10, 100), sell(4, 500)])
    assert amount == 6
    assert avg == 100


def test_selling_everything_leaves_an_empty_position():
    amount, avg = aggregate_transactions([buy(10, 100), sell(10, 500)])
    assert amount == 0
    assert avg == 100


def test_coverage_accepts_a_chain_that_stays_positive():
    check_coverage([buy(10, 100), sell(4), buy(5, 200), sell(11)], "bitcoin")


def test_coverage_rejects_a_sell_that_exceeds_the_amount_held():
    with pytest.raises(InsufficientHoldingAmount):
        check_coverage([buy(10, 100), sell(11)], "bitcoin")


def test_a_later_buy_does_not_cover_an_earlier_sell():
    with pytest.raises(InsufficientHoldingAmount):
        check_coverage([buy(2.5, 100), sell(4), buy(5, 200)], "bitcoin")


def test_float_noise_does_not_count_as_overselling():
    # 0.3 - 0.1 - 0.2 lands just below zero in binary floating point.
    check_coverage([buy(0.3, 100), sell(0.1), sell(0.2)], "bitcoin")


def test_order_of_buy_and_sell_matters():
    txs = [buy(10, 100), buy(10, 200), sell(5)]
    buy_first_amount, buy_first_avg = aggregate_transactions(txs)

    txs = [buy(10, 100), sell(5), buy(10, 200)]
    sell_first_amount, sell_first_avg = aggregate_transactions(txs)

    assert buy_first_amount == sell_first_amount == 15
    assert buy_first_avg == 150
    assert sell_first_avg == pytest.approx(166.667, abs=0.001)
