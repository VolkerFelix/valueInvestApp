import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

    assert intrinsic_value.m_intrinsic_value != 0.0, "Intrinsic value was not calculated."
    assert intrinsic_value.m_market_cap != 0.0, "Market cap was not calculated."
    assert intrinsic_value.m_safety_margin != 0.0, "Safety margin was not calculated."
    assert isinstance(intrinsic_value.m_undervalued, bool), "Undervalued not calculated."







