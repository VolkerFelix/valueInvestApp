import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from web_scrape.yahooAnalysis import Analysis

#COMPANY_SYMBOL = "BAYN.DE"
COMPANY_SYMBOL = "MSFT"

def test_analysis():
    growth_rate = Analysis(COMPANY_SYMBOL)
    print("Growth rate: ", growth_rate)

    assert growth_rate != 0.0, "Growth rate should be different than zero."







