from bs4 import ResultSet, BeautifulSoup
import requests
import pandas as pd
from io import StringIO
#from web_scrape.scrape import scrape_table, string_to_float
from scrape import scrape_table, string_to_float, scrape_headers

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


class Analysis:
    def __init__(self, f_symbol: str):
        self.m_symbol = f_symbol
        self.m_growth_estimates = None
        self.__load_analysis()

    def __get_yahoo_analysis_growth_estimates(self) -> None:
        # This part is not implemented by yFinance --> Fallback to ByteSoup
        url = f"https://finance.yahoo.com/quote/{self.m_symbol}/analysis"
        tables = scrape_table(url)
        for table in tables:
            # Convert each table into a DataFrame
            df = pd.read_html(StringIO(str(table)))[0]
            if any(df.astype(str).apply(lambda x: x.str.contains("Next 5 Years", case=False, na=False)).any()):
                df.rename(columns={'CURRENCY IN USD': 'Growth Estimates'}, inplace=True)
                self.m_growth_estimates = df
                return
                        
        # Set to None if not found
        self.m_growth_estimates = None

    def __load_analysis(self) -> None:
        # Load growth estimates
        self.__get_yahoo_analysis_growth_estimates()

    def get_growth_rate_estimate_5_year_avg(self) -> float:
        try:
            next_5_y = self.m_growth_estimates[self.m_growth_estimates['Growth Estimates'] == 'Next 5 Years (per annum)'].iloc[0,1]
            return string_to_float(next_5_y)
        except Exception:
            return None
    
if __name__ == "__main__":
    growth_rate = Analysis("MSFT").get_growth_rate_estimate_5_year_avg()
    print(growth_rate)