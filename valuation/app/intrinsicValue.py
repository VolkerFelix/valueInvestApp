from typing import List
import statistics
from yahooFinancials import YahooFinancialStats
from wacc import get_wacc

def get_expected_fcf_for_n_years(f_current_fcf: float, f_growth_rate: float, f_years: int) -> List[float]:
    future_fcf = [f_current_fcf]
    for i in range(f_years):
        future_fcf.append(future_fcf[i] * (1 + f_growth_rate))
    return future_fcf

def calc_discounted_cash_flows(f_cash_flows: List[float], f_wacc: float) -> List[float]:
    discounted_cf = []
    for i, value in enumerate(f_cash_flows):
        discounted_cf.append(value/pow((1 + f_wacc),i))
    return discounted_cf

class IntrinsicValue:
    
    def __init__(
            self,
            f_company_symbol: str,
            f_expected_growth: float,
            f_time_span_years: int
    ):
        # Init company
        self.m_company = YahooFinancialStats(f_company_symbol)
        self.m_expected_growth = f_expected_growth
        self.m_time_span = f_time_span_years
        self.m_intrinsic_value = 0.0
        self.m_market_cap = 0.0

        self._calc()

    def _calc(self) -> None:
        # Predict future cash flows
        ## Get average over the past free cash flows
        fcf_all = self.m_company.get_fcf()
        fcf_avg = statistics.mean(fcf_all)
        # Get expected cash flows for the next n years
        future_fcf = get_expected_fcf_for_n_years(fcf_avg, self.m_expected_growth, self.m_time_span)
        # Get discounted cash flows
        wacc = get_wacc(self.m_company)
        fcf_future_discounted = calc_discounted_cash_flows(future_fcf, wacc)
        # Calc terminal value
        self.m_market_cap = round(self.m_company.get_market_cap(), 2)
        price_to_fcf_ratio = self.m_market_cap / fcf_all[0]
        # Terminal value: Last discounted fcf x price to fcf ratio = selling price
        terminal_value = fcf_future_discounted[-1] * price_to_fcf_ratio
        # Sum up all discounted fcf
        sum_discounted_fcf = 0
        for fcf in fcf_future_discounted : sum_discounted_fcf += fcf
        # Instrinsic value = Sum of discounted cash flows + terminal value
        intrinsic_value = sum_discounted_fcf + terminal_value
        # Cash reserves of the company need to be added as well
        cash = self.m_company.get_total_cash()

        self.m_intrinsic_value = round(intrinsic_value + cash, 2)