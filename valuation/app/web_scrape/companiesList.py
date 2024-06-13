from bs4 import ResultSet
from web_scrape.scrape import scrape_table

INDEX_URL_MAP = {
    'SP500': 'https://stockanalysis.com/list/sp-500-stocks',
    'DAX': 'https://en.wikipedia.org/wiki/DAX'
}

INDEX_AVG_HIST_GROWTH_MAP = {
    'SP500': 0.1026,
    'DAX': 0.0804
}

def _dax_get_names_and_symbols(f_scrapped_table: ResultSet) -> dict:
    result = {}
    for table in f_scrapped_table:
        # Scrape all rows
        trs = table.find_all('tr')
        for tr in trs:
            # Scrape all table data tags
            tds = tr.find_all('td')
            # Index 1 of tds contains the company's name
            # Index 3 of tds contains the company's symbol
            if not tds:
                continue
            name = tds[1].get_text()
            symbol = tds[3].get_text()
            result[name] = symbol

    return result

def _sp500_get_names_and_symbols(f_scrapped_table: ResultSet) -> dict:
    result = {}
    for table in f_scrapped_table:
        trs = table.find_all('tr')
        for tr in trs:
            tds = tr.find_all('td')
            if not tds:
                continue
            name = tds[2].get_text().strip()
            symbol = tds[1].get_text()
            symbol = symbol.replace('.','-')
            result[name] = symbol
    
    return result

class CompaniesList:
    def __init__(self, f_index_name: str):
        self.m_companies = {}
        try:
            self.m_index_url = INDEX_URL_MAP[f_index_name]
            self.m_avg_growth_rate = INDEX_AVG_HIST_GROWTH_MAP[f_index_name]
        except KeyError:
            print("Index name not found.")

        self._get_all_companies(f_index_name)

    def _get_all_companies(self, f_index_name: str):
        if f_index_name == 'DAX':
            self.m_companies = _dax_get_names_and_symbols(scrape_table(self.m_index_url, "constituents"))
        elif f_index_name == 'SP500':
            self.m_companies =  _sp500_get_names_and_symbols(scrape_table(self.m_index_url))
        else:
            AssertionError(f"Index {f_index_name} not implemented.")