from bs4 import ResultSet
from scrape import scrape_table
import pprint

# Simulate browser
HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0'
}

def get_yahoo_analysis(f_symbol: str) -> ResultSet:
    url = f"https://finance.yahoo.com/quote/{f_symbol}/analysis"
    return scrape_table(url)

class Analysis:
    def __init__(self, f_symbol: str):
        self.m_data = {}
        self._load_analysis(f_symbol)

    def _load_analysis(self, f_symbol: str) -> None:
        scraped_data = get_yahoo_analysis(f_symbol)
        for table in scraped_data:
            # Scrape all table rows into variable trs
            trs = table.find_all('tr')
            section_name = ''
            for tr in trs:
                # Get table headers and use as section info
                ths = tr.find_all('th')
                if ths:
                    section_name = tr.find_all('th')[0].get_text().strip()
                    self.m_data[section_name] = {}
                # Scrape all table data tags into variable tds
                tds = tr.find_all('td')
                if not tds:
                    continue
                self.m_data[section_name][tds[0].get_text().strip()] = [tds[1].get_text(), tds[2].get_text(), tds[3].get_text(), tds[4].get_text()]
