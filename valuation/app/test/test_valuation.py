import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pprint

from web_scrape.forecast import Analysis
from intrinsic_value.intrinsicValue import IntrinsicValue

GROWTH_RATE = 0.1026
TIME_SPAN = 5
COMPANY_SYMBOL = "BAYN.DE"
COMPANY_NAME = "Bayer"

def test_intrinsic_value():
    yahoo_analysis = Analysis(COMPANY_SYMBOL)
    growth_rate_yahoo = yahoo_analysis.get_expected_growth_rate_over_5_years_per_annum()
    intrinsic_value = IntrinsicValue(COMPANY_SYMBOL, growth_rate_yahoo, TIME_SPAN)

    stock = {
        "m_name": COMPANY_NAME,
        "m_description": "",
        "m_intrinsic_value": intrinsic_value.m_intrinsic_value,
        "m_current_market_cap": intrinsic_value.m_market_cap,
        "m_safety_margin": intrinsic_value.m_safety_margin,
        "m_undervalued": intrinsic_value.m_undervalued,
        "m_over_timespan": TIME_SPAN,
        "m_used_growth_rate_annual": growth_rate_yahoo,
        "m_assumed_growth_rate_company_annual": growth_rate_yahoo
    }

    pprint.pprint(stock)




