from bs4 import ResultSet
from web_scrape.scrape import scrape_table

# Simulate browser
HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0'
}

def get_all_companies(f_index_url: str) -> ResultSet:
    if 'DAX' in f_index_url:
         return scrape_table(f_index_url, "constituents")
    else:
        return scrape_table(f_index_url)    

class CompaniesList:
    def __init__(self, f_list_name: str):
        self.m_companies = {}
        self._load_names_and_symbols(f_list_name)

    def _load_names_and_symbols(self, f_list_name: str) -> None:
        scraped_data = get_all_companies(f_list_name)
        for table in scraped_data:
            # Scrape all table rows into variable trs
            trs = table.find_all('tr')
            for tr in trs:
                # Scrape all table data tags into variable tds
                tds = tr.find_all('td')
                # Index 0 of tds will contain the measurement
                # Index 1 of tds will contain the value
                if not tds:
                    continue
                name = tds[2].get_text().strip()
                symbol = tds[1].get_text()
                symbol = symbol.replace('.','-')
                self.m_companies[name] = symbol

