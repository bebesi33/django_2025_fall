import unittest
from src.loan_calc import calculate_annuity_installment


INTEREST_RATES = [0.0, 0.1, 0.3]
TENORS = [1.0, 0.5, 7.0]
EXPECTED_VALUES = [833.3333333333334, 1715.613941855922, 285.92979317120717]


class NotableTestCases(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.notional = 10000
        cls.installment_frequency = 12

    @classmethod
    def method_factory(cls, interest_rate: float, tenor: float, expected_result: float):
        def calculation_case_generator(cls):
            result_value = calculate_annuity_installment(
                cls.notional, interest_rate, tenor, cls.installment_frequency
            )
            cls.assertAlmostEqual(result_value, expected_result, places=5)

        return calculation_case_generator


for interest_rate, tenor, expected_result in zip(
    INTEREST_RATES, TENORS, EXPECTED_VALUES
):
    func = NotableTestCases.method_factory(interest_rate, tenor, expected_result)
    setattr(NotableTestCases, f"test_ir_{interest_rate}_tenor_{tenor}", func)


if __name__ == "__main__":
    unittest.main()
