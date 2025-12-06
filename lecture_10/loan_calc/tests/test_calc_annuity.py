import unittest

from src.loan_calc import calculate_annuity_installment


class TestCalculateAnnuityInstallment(unittest.TestCase):

    def setUp(self):
        self.notional = 40000000

    def test_calculate_annuity_installment_happy(self):
        payment = calculate_annuity_installment(
            principal=self.notional, tenor=20, interest_rate=0.0599, installment_frequency=12
        )
        # self.assertTrue(abs(payment - 286341.7089640132) < 0.00001)
        self.assertAlmostEqual(payment, 286341.7089640132, places=5)

    def test_negative_interest_rate(self):
        # Test with negative interest rate (should raise ValueError)
        # Notice that the test checks whether the ValueError is generated
        interest_rate = -0.05
        tenor = 10.0
        installment_frequency = 12
        with self.assertRaises(ValueError):
            calculate_annuity_installment(self.notional, interest_rate, tenor, installment_frequency)

    def test_calculate_zero_rate(self):
        payment = calculate_annuity_installment(
            principal=10000000, tenor=20, interest_rate=0.000, installment_frequency=12
        )
        self.assertAlmostEqual(payment, 41666.66666666, places=5)
