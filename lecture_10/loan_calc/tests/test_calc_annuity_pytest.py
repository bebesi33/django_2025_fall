import pytest
from src.loan_calc import calculate_annuity_installment


@pytest.fixture
def notional():
    return 40000000


def test_calculate_annuity_installment_happy_2(notional):
    result_value = calculate_annuity_installment(
        notional, interest_rate=0.0599, tenor=20, installment_frequency=12
    )
    assert pytest.approx(result_value, rel=1e-5) == 286341.7089640132
