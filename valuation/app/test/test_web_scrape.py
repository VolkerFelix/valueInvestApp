import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from web_scrape.companiesList import CompaniesList

INDEX_NAME = "SP500"

def test_companies_list():
    items = CompaniesList(INDEX_NAME).m_companies.items()

    assert items, "No stocks fetched."







