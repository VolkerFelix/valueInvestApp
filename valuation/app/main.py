from db_interface.stock_db_interface import rquest_access_token, create_new_stock
from intrinsic_value.intrinsicValue import IntrinsicValue
from db_interface.stock_db_interface import StockDBFormat
from web_scrape.companiesList import CompaniesList
from web_scrape.forecast import Analysis
from typing import List
from decimal import *

COMPANY_LIST_NAMES_MAP = {
    'S&P500': 'sp-500-stocks'
}

# Define an expected growth rate
## S&P500 average since 1957 = 10.26%
SP500_GROWTH_AVG = 0.1026
# Time span in years for valuation
TIME_SPAN = 5

if __name__ == '__main__':
    bearer = ''
    counter = 0

    for list_name, list_symbol in COMPANY_LIST_NAMES_MAP.items():
        list = CompaniesList(list_symbol)
        for company_name, symbol in list.m_companies.items():
            print(company_name)
            print(symbol)
            yahoo_analysis = Analysis(symbol)
            growth_rate = SP500_GROWTH_AVG
            growth_rate_yahoo = yahoo_analysis.get_expected_growth_rate_over_5_years_per_annum()
            if not growth_rate:
                growth_rate_yahoo = 0.0
            intrinsic_value = IntrinsicValue(symbol, growth_rate, TIME_SPAN)

            stock = {
                "m_name": company_name,
                "m_description": "",
                "m_intrinsic_value": intrinsic_value.m_intrinsic_value,
                "m_current_market_cap": intrinsic_value.m_market_cap,
                "m_safety_margin": intrinsic_value.m_safety_margin,
                "m_undervalued": intrinsic_value.m_undervalued,
                "m_over_timespan": TIME_SPAN,
                "m_used_growth_rate_annual": growth_rate,
                "m_assumed_growth_rate_company_annual": growth_rate_yahoo
            }

            if not bearer:
                # Request access token
                respone = rquest_access_token()
                print(respone.json())
                bearer = respone.json()['access_token']
            
            status_code = create_new_stock(StockDBFormat(**stock), bearer)
            counter += 1
            print(status_code)
            print(counter)
