import unittest
from unittest import mock
import os
import pandas as pd
from pandas.testing import assert_frame_equal
from pathlib import Path
from src.loan_calc import calculate_annuity_cashflow_decomposition


ABSOLUTE_PATH = Path(os.path.dirname(__file__))


@mock.patch(
    target="src.loan_calc.calculate_annuity_installment",
    return_value=285.92979317120717,
)
class TestCf(unittest.TestCase):
    def test_cf_decomposition(self, mock_installment):
        decomp_result = calculate_annuity_cashflow_decomposition(
            principal=10000, interest_rate=0.3, tenor=7, installment_frequency=12
        )
        expected_result = pd.read_csv(
            ABSOLUTE_PATH / "resources" / "cf_test_case_1.csv"
        )
        assert_frame_equal(
            expected_result, decomp_result, check_exact=False, rtol=0.001
        )
        assert mock_installment.called
