import unittest
from src.loan_calc import calculate_annuity_installment


class TestCalculateAnnuityInstallment(unittest.TestCase):
    def test_positive_interest_rate(self):
        # Test with positive interest rate
        principal = 100000.0
        interest_rate = 0.05
        tenor = 10.0
        installment_frequency = 12
        expected_result = 1060.66  # Expected monthly installment
        result_value = calculate_annuity_installment(principal, interest_rate, tenor, installment_frequency)
        self.assertAlmostEqual(result_value, expected_result, places=2)

    def test_zero_interest_rate(self):
        # Test with zero interest rate
        # Notice that we only test the value of this up until 2 decimal places
        principal = 100000.0
        interest_rate = 0.0
        tenor = 10.0
        installment_frequency = 12
        expected_result = 833.33  # Expected monthly installment
        result_value = calculate_annuity_installment(principal, interest_rate, tenor, installment_frequency)
        self.assertAlmostEqual(result_value, expected_result, places=2)

    def test_negative_tenor(self):
        # Test with negative tenor (should raise ValueError)
        principal = 100000.0
        interest_rate = 0.05
        tenor = -5.0
        installment_frequency = 12
        with self.assertRaises(ValueError):
            calculate_annuity_installment(principal, interest_rate, tenor, installment_frequency)

    def test_negative_interest_rate(self):
        # Test with negative interest rate (should raise ValueError)
        # Notice that the test checks whether the ValueError is generated
        principal = 100000.0
        interest_rate = -0.05
        tenor = 10.0
        installment_frequency = 12
        with self.assertRaises(ValueError):
            calculate_annuity_installment(principal, interest_rate, tenor, installment_frequency)

    def test_zero_tenor(self):
        # Test with zero tenor (should raise ValueError)
        principal = 100000.0
        interest_rate = 0.05
        tenor = 0.0
        installment_frequency = 12
        with self.assertRaises(ValueError):
            calculate_annuity_installment(principal, interest_rate, tenor, installment_frequency)

if __name__ == "__main__":
    unittest.main()
