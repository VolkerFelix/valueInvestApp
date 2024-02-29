import pandas as pd
from wacc import get_wacc
from yahooFinancials import YahooFinancialStats, BILLION
from db_interface import rquest_access_token, create_new_stock
import statistics
from typing import List

# Margin for error in valuation calc
SAFETY_MARGIN = 0.5
# Define an expected growth rate
## S&P500 average since 1957 = 10.26%
GROWTH_EXPECTED = 0.1026
# Time span in years for valuation
TIME_SPAN = 5

company_symbol_map = {
    'Nvidia': 'NVDA',
    'AMD': 'AMD',
    'ARM': 'ARM',
    'Qualcomm': 'QCOM'
}

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

if __name__ == '__main__':
    bearer = ''
    for company_name, symbol in company_symbol_map.items():
        # Init company
        company = YahooFinancialStats(symbol)
        # Predict future cash flows
        ## Get average over the past free cash flows
        fcf_all = company.get_fcf()
        fcf_avg = statistics.mean(fcf_all)
        # Get expected cash flows for the next n years
        future_fcf = get_expected_fcf_for_n_years(fcf_avg, GROWTH_EXPECTED, TIME_SPAN)
        # Get discounted cash flows
        wacc = get_wacc(company)
        fcf_future_discounted = calc_discounted_cash_flows(future_fcf, wacc)
        # Calc terminal value
        market_cap = company.get_market_cap()
        price_to_fcf_ratio = market_cap / fcf_all[0]
        # Terminal value: Last discounted fcf x price to fcf ratio = selling price
        terminal_value = fcf_future_discounted[-1] * price_to_fcf_ratio
        # Sum up all discounted fcf
        sum_discounted_fcf = 0
        for fcf in fcf_future_discounted : sum_discounted_fcf += fcf
        # Instrinsic value = Sum of discounted cash flows + terminal value
        intrinsic_value = sum_discounted_fcf + terminal_value
        # Cash reserves of the company need to be added as well
        cash = company.get_total_cash()
        intrinsic_value += cash

        intrinsic_value_incl_safety = intrinsic_value * SAFETY_MARGIN

        print(f"Intrinsic value of {company_name} in B$:")
        print("%.2f" % (intrinsic_value / BILLION))
        print("Market Cap in B$:")
        print("%.2f" % (market_cap / BILLION))
        print("Safety margin in %:")
        print("%.2f" % ((intrinsic_value - market_cap) / intrinsic_value * 100.0))

        new_stock = {
            "m_name": "Test Stock",
            "m_description": "For testing",
            "m_intrinsic_value": 50.0,
            "m_current_market_cap": 25.0,
            "m_safety_margin": 0.5,
            "m_over_timespan": 5,
            "m_assumed_growth_rate_anual": 0.1
        }

        if not bearer:
            # Request access token
            respone = rquest_access_token()
            print(respone.json())
            bearer = respone.json()['access_token']
        
        status_code = create_new_stock(new_stock, bearer)
        print(status_code)
