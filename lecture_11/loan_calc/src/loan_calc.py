import logging
import pandas as pd

logger = logging.getLogger(__name__)
EPSILON = 10e-15


def calculate_annuity_installment(
    principal: float,
    interest_rate: float,
    tenor: int = 10.0,
    installment_frequency: int = 12,
) -> float:
    """
    Calculates the monthly installment for an annuity.

    Args:
        principal (float): The initial loan amount.
        interest_rate (float): Annual interest rate (expressed as a decimal, e.g., 0.05 for 5%).
        tenor (int): The term of a loan in X years.
        installment_frequency (int): number of installments in a year

    Returns:
        float: Monthly installment amount.
    """
    if tenor <= 0.0:
        raise ValueError("The tenor of the loan should be a positive number!")

    if interest_rate < 0.0:
        raise ValueError("Interest rate must be non-negative!")

    # Calculate result when we have a loan with zero interest rate
    if abs(interest_rate - 0.0) < EPSILON:
        annuity_installment = principal / (installment_frequency * tenor)
        return annuity_installment

    # Calculate monthly interest rate
    monthly_interest_rate = interest_rate / installment_frequency

    # Calculate annuity installment
    annuity_installment = (principal * monthly_interest_rate) / (
        1 - (1 + monthly_interest_rate) ** -(installment_frequency * tenor)
    )

    return annuity_installment


def calculate_annuity_cashflow_decomposition(
    principal: float,
    interest_rate: float,
    tenor: int = 10.0,
    installment_frequency: int = 12,
) -> pd.DataFrame:
    """
    Calculates the monthly installment and interest payment for an annuity.

    Args:
        principal (float): The initial loan amount.
        interest_rate (float): Annual interest rate (expressed as a decimal, e.g., 0.05 for 5%).
        tenor (int): The term of a loan in X years.
        installment_frequency (int): number of installments in a year

    Returns:
        pd.DataFrame: dataframe 
    """    
    installment = calculate_annuity_installment(
        principal, interest_rate, tenor, installment_frequency
    )
    logger.warning(f"Calculated installment is {installment}")
    time_periods = list(range(1, 1 + tenor * installment_frequency))
    total_cf = [installment] * (tenor * installment_frequency)
    interest_cf = []
    principal_cf = []
    monthly_interest_rate = interest_rate / installment_frequency
    remaining_notional = principal
    for installment in total_cf:
        interest = remaining_notional * monthly_interest_rate
        principal_repayed = installment - interest
        interest_cf.append(interest)
        principal_cf.append(principal_repayed)
        remaining_notional -= principal_repayed

    return pd.DataFrame(
        {
            "time_period": time_periods,
            "insterest_cf": interest_cf,
            "principal_cf": principal_cf,
        }
    )
