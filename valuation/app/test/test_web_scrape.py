import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from web_scrape.companiesList import CompaniesList

STOCKS_PER_INDEX = {
    "SP500": 500,
    "DAX": 40
}

def test_companies_list():
    fetched_amount = 0
    desired_amount = 0
    for index_name, stock_amount in STOCKS_PER_INDEX.items():
        fetched_amount += len(CompaniesList(index_name).m_companies.items())
        desired_amount += stock_amount

    assert desired_amount==fetched_amount, "Not all stocks fetched!"







