import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from intrinsic_value.intrinsicValue import IntrinsicValue

GROWTH_RATE = 0.1026
TIME_SPAN = 5
#COMPANY_SYMBOL = "BAYN.DE"
COMPANY_SYMBOL = "MSFT"

def test_intrinsic_value():
    intrinsic_value = IntrinsicValue(COMPANY_SYMBOL, GROWTH_RATE, TIME_SPAN)

    assert intrinsic_value.m_intrinsic_value != 0.0, "Intrinsic value was not calculated."
    assert intrinsic_value.m_market_cap != 0.0, "Market cap was not calculated."
    assert intrinsic_value.m_safety_margin != 0.0, "Safety margin was not calculated."
    assert isinstance(intrinsic_value.m_undervalued, bool), "Undervalued not calculated."







