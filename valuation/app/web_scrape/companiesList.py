from bs4 import ResultSet
from web_scrape.scrape import scrape_table

INDEX_URL_MAP = {
    'SP500': 'https://stockanalysis.com/list/sp-500-stocks',
    'DAX': 'https://en.wikipedia.org/wiki/DAX'
}

def __dax_get_names_and_symbols(f_scrapped_table: ResultSet) -> dict:
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

def __sp500_get_names_and_symbols(f_scrapped_table: ResultSet) -> dict:
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

def get_all_companies(f_index_name: str, f_index_url: str) -> dict:
    result = {}
    if f_index_name == 'DAX':
        result = __dax_get_names_and_symbols(scrape_table(f_index_url, "constituents"))
    elif f_index_name == 'SP500':
        result =  __sp500_get_names_and_symbols(scrape_table(f_index_url))
    else:
        assert False, f"Index {f_index_name} not implemented."
    
    return result

class CompaniesList:
    def __init__(self, f_index_name: str):
        self.m_companies = {}
        index_url = ''
        try:
            index_url = INDEX_URL_MAP[f_index_name]
        except KeyError:
            print("Index name not found.")
        self.m_companies = get_all_companies(f_index_name, index_url)

