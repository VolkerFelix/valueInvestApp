import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from web_scrape.yahooAnalysis import Analysis

TEST_COMPANIES = [
    "MSFT",
    "LUV"
]

def test_analysis():
    for company in TEST_COMPANIES:
        analysis = Analysis(company)
        assert analysis.get_growth_rate_estimate_next_5_y != None, "Future growth rate not calculated."
        assert analysis.get_growth_rate_estimate_past_5_y != None, "Past growth rate not calculated."







