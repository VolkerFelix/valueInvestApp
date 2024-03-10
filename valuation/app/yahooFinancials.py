import requests
from bs4 import BeautifulSoup, ResultSet
from typing import List
from scrape import scrape_table, scrape_div_by_title

THOUSAND = 1000
MILLION = THOUSAND * 1000
BILLION = MILLION * 1000
TRILLION = BILLION * 1000

# Simulate browser
HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0'
}

BASE_BETA_URL = "https://finance.yahoo.com/quote/"

FINANCIALS_TAB_MAP = {
    "Operating Expense": "financials",
    "Operating Income": "financials",
    "Free Cash Flow": "cash-flow",
    "Pretax Income": "financials",
    "Tax Provision": "financials",
    "Total Debt": "balance-sheet",
    "Total Equity Gross Minority Interest": "balance-sheet"
}

def scrape_statistics(f_symbol: str) -> ResultSet:
    url = f"{BASE_BETA_URL}{f_symbol}/key-statistics"
    return scrape_table(url)

def scrape_financials(f_symbol: str, f_title: str) -> ResultSet:
    url = f"{BASE_BETA_URL}{f_symbol}/{FINANCIALS_TAB_MAP[f_title]}"
    return scrape_div_by_title(url, f_title)

class YahooFinancialStats:
    def __init__(self, f_symbol: str):
        print("Yahoo Finance: " + f_symbol)
        self.m_financials = {}
        self._load_financials(f_symbol, list(FINANCIALS_TAB_MAP.keys()))
        self.m_key_statistics = {}
        self._load_key_statistics(f_symbol)

    def _load_financials(self, f_symbol: str, f_titles: List[str]) -> None:
        for title in f_titles:
            scraped_data = scrape_financials(f_symbol, title)
            values = []
            for element in scraped_data:
                # Get the whole row
                grand_parent = element.parent.parent
                for item in grand_parent:
                    try:
                        content = item.find_all("span")[0].get_text().strip()
                    except IndexError:
                        # No data available for this year
                        continue
                    if content == title:
                        continue
                    values.append(string_to_float(content, f_scale=THOUSAND))

            self.m_financials[title] = values

    def _load_key_statistics(self, f_symbol: str) -> None:
        scraped_data = scrape_statistics(f_symbol)
        for table in scraped_data:
            # Scrape all table rows into variable trs
            trs = table.find_all('tr')
            for tr in trs:
                # Scrape all table data tags into variable tds
                tds = tr.find_all('td')
                # Index 0 of tds will contain the measurement
                # Index 1 of tds will contain the value
                self.m_key_statistics[tds[0].get_text().strip()] = tds[1].get_text()

    def get_beta(self) -> float:
        beta = self.m_key_statistics['Beta (5Y Monthly)']
        if beta == 'N/A':
            beta = 1.0
        return float(beta)
    
    def get_op_ex(self) -> List[float]:
        return self.m_financials['Operating Expense']
    
    def get_op_income(self) -> List[float]:
        return self.m_financials['Operating Income']
    
    def get_fcf(self) -> List[float]:
        return self.m_financials['Free Cash Flow']
    
    def get_market_cap(self) -> float:
        return string_to_float(self.m_key_statistics['Market Cap (intraday)'])
    
    def get_total_cash(self) -> float:
        return string_to_float(self.m_key_statistics['Total Cash (mrq)'])
    
    def get_ebt(self) -> List[float]:
        return self.m_financials['Pretax Income']
    
    def get_tax_provision(self) -> List[float]:
        return self.m_financials['Tax Provision']
    
    def get_total_debt(self) -> List[float]:
        total_debt = self.m_financials['Total Debt']
        if not total_debt:
            # Set to 0 since we don't know any better
            total_debt = [0.0]
        return total_debt
    
    def get_total_equity(self) -> float:
        return self.m_financials['Total Equity Gross Minority Interest']
    
def string_to_float(f_value: str, f_scale: float = 1.0) -> float:
        value_f = 0.0
        if "T" in f_value:
            value_f = float(f_value.replace('T','')) * TRILLION
        elif "B" in f_value: 
            value_f = float(f_value.replace('B','')) * BILLION
        elif "M" in f_value: 
            value_f = float(f_value.replace('M','')) * MILLION
        elif "," in f_value: 
            value_f = float(f_value.replace(',',''))
        elif "N/A" in f_value: 
            value_f = 0.0
        else:
            assert False, f"Amount not defined"

        return value_f * f_scale