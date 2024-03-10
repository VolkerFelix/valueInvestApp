from yahooFinancials import YahooFinancialStats, BILLION
from stock_db_interface import rquest_access_token, create_new_stock
from intrinsicValue import IntrinsicValue
from stock_db_interface import StockDBFormat
from companiesList import CompaniesList
from typing import List
from decimal import *

COMPANY_LIST_NAMES_MAP = {
    'S&P500': 'sp-500-stocks'
}

# Define an expected growth rate
## S&P500 average since 1957 = 10.26%
GROWTH_EXPECTED = 0.1026
# Time span in years for valuation
TIME_SPAN = 5

if __name__ == '__main__':
    bearer = ''

    for list_name, list_symbol in COMPANY_LIST_NAMES_MAP.items():
        list = CompaniesList(list_symbol)
        for company_name, symbol in list.m_companies.items():
            intrinsic_value = IntrinsicValue(symbol, GROWTH_EXPECTED, TIME_SPAN)

            stock = {
                "m_name": company_name,
                "m_description": "",
                "m_intrinsic_value": intrinsic_value.m_intrinsic_value,
                "m_current_market_cap": intrinsic_value.m_market_cap,
                "m_safety_margin": intrinsic_value.m_safety_margin,
                "m_undervalued": intrinsic_value.m_undervalued,
                "m_over_timespan": TIME_SPAN,
                "m_assumed_growth_rate_anual": GROWTH_EXPECTED
            }

            if not bearer:
                # Request access token
                respone = rquest_access_token()
                print(respone.json())
                bearer = respone.json()['access_token']
            
            status_code = create_new_stock(StockDBFormat(**stock), bearer)
            print(company_name)
            print(status_code)
