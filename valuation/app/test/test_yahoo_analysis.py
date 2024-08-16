import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from web_scrape.yahooAnalysis import Analysis

#COMPANY_SYMBOL = "BAYN.DE"
COMPANY_SYMBOL = "MSFT"

def test_analysis():
    company = Analysis(COMPANY_SYMBOL)
    future_growth = company.get_growth_rate_estimate_next_5_y()
    past_growth = company.get_growth_rate_estimate_past_5_y()
    assert isinstance(future_growth, float)
    assert isinstance(past_growth, float)
    assert future_growth != 0.0, "Future growth rate should be different than zero."
    assert past_growth != 0.0, "Future growth rate should be different than zero."







