import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from web_scrape.forecast import Analysis

def test_analysis():
    symbol = 'SYF'
    company = Analysis(symbol)
    growth_rate = company.get_expected_growth_rate_over_5_years_per_annum()
    growth_rate_past = company.get_growth_rate_over_past_5_years_per_annum()
    print("Growth rate: " + str(growth_rate))
    print("Growth rate past: " + str(growth_rate_past))
    assert isinstance(growth_rate, float), "Should be a float"
    assert isinstance(growth_rate_past, float), "Should be a float"
    