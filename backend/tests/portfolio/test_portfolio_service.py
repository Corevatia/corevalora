from services.portfolio_service import compute_avg_price


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
