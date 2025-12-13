import pytest
from src.loan_calc import calculate_annuity_installment

INTEREST_RATES = [0.0, 0.1, 0.3]
TENORS = [1.0, 0.5, 7.0]
EXPECTED_VALUES = [833.3333333333334, 1715.613941855922, 285.92979317120717]


@pytest.fixture
def installment_frequency():
    return 12


@pytest.fixture
def notional():
    return 10000


@pytest.mark.parametrize(
    "interest_rate, tenor, expected_result",
    zip(INTEREST_RATES, TENORS, EXPECTED_VALUES),
)
def test_calculate_annuity_installment(
    interest_rate, tenor, expected_result, installment_frequency, notional
):
    # notional = 10000
    # installment_frequency = 12
    result_value = calculate_annuity_installment(
        notional, interest_rate, tenor, installment_frequency
    )
    assert pytest.approx(result_value, rel=1e-5) == expected_result
