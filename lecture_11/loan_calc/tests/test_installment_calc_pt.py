import pytest
from src.loan_calc import calculate_annuity_installment


class TestCalculateAnnuityInstallment:
    def test_positive_interest_rate(self):
        # Test with positive interest rate
        principal = 100000.0
        interest_rate = 0.05
        tenor = 10.0
        installment_frequency = 12
        expected_result = 1060.66  # Expected monthly installment
        result = calculate_annuity_installment(
            principal, interest_rate, tenor, installment_frequency
        )
        assert pytest.approx(result, rel=1e-2) == expected_result

    def test_zero_interest_rate(self):
        # Test with zero interest rate
        principal = 100000.0
        interest_rate = 0.0
        tenor = 10.0
        installment_frequency = 12
        expected_result = 833.33  # Expected monthly installment
        result = calculate_annuity_installment(
            principal, interest_rate, tenor, installment_frequency
        )
        assert pytest.approx(result, rel=1e-2) == expected_result

    def test_negative_tenor(self):
        # Test with negative tenor (should raise ValueError)
        principal = 100000.0
        interest_rate = 0.05
        tenor = -5.0
        installment_frequency = 12
        with pytest.raises(ValueError):
            calculate_annuity_installment(
                principal, interest_rate, tenor, installment_frequency
            )

    def test_negative_interest_rate(self):
        # Test with negative interest rate (should raise ValueError)
        principal = 100000.0
        interest_rate = -0.05
        tenor = 10.0
        installment_frequency = 12
        with pytest.raises(ValueError):
            calculate_annuity_installment(
                principal, interest_rate, tenor, installment_frequency
            )

    def test_zero_tenor(self):
        # Test with zero tenor (should raise ValueError)
        principal = 100000.0
        interest_rate = 0.05
        tenor = 0.0
        installment_frequency = 12
        with pytest.raises(ValueError):
            calculate_annuity_installment(
                principal, interest_rate, tenor, installment_frequency
            )
