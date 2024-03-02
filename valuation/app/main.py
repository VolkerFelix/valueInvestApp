from yahooFinancials import YahooFinancialStats, BILLION
from stock_db_interface import rquest_access_token, create_new_stock
from intrinsicValue import IntrinsicValue
from typing import List
from decimal import *

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

if __name__ == '__main__':
    bearer = ''
    for company_name, symbol in company_symbol_map.items():
        stock = IntrinsicValue(symbol, GROWTH_EXPECTED, TIME_SPAN)
        safety_margin = (stock.m_intrinsic_value - stock.m_market_cap) / stock.m_intrinsic_value * 100.0

        print(f"Intrinsic value of {company_name} in B$:")
        print(stock.m_intrinsic_value / BILLION)
        print("Market Cap in B$:")
        print(stock.m_market_cap / BILLION)
        print("Safety margin in %:")
        print(safety_margin)

        new_stock = {
            "m_name": company_name,
            "m_description": "",
            "m_intrinsic_value": stock.m_intrinsic_value,
            "m_current_market_cap": stock.m_market_cap,
            "m_safety_margin": safety_margin,
            "m_over_timespan": TIME_SPAN,
            "m_assumed_growth_rate_anual": GROWTH_EXPECTED
        }

        if not bearer:
            # Request access token
            respone = rquest_access_token()
            print(respone.json())
            bearer = respone.json()['access_token']
        
        status_code = create_new_stock(new_stock, bearer)
        print(status_code)
