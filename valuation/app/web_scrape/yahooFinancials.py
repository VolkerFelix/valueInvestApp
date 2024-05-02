import pandas as pd
import yfinance as yf

class YahooFinancialStats:
    def __init__(self, f_symbol: str):
        self.m_ticker = yf.Ticker(f_symbol)

    def get_beta(self) -> float:
        return self.m_ticker.info['beta']
    
    def get_market_cap(self) -> int:
        return self.m_ticker.info['marketCap']
    
    def get_total_cash(self) -> int:
        return self.m_ticker.info['totalCash']
    
    def get_fcf(self) -> pd.DataFrame:
        return self.m_ticker.get_cash_flow().loc['FreeCashFlow']
    
    def get_ebt(self) -> pd.DataFrame:
        return self.m_ticker.get_financials().loc['PretaxIncome']
    
    def get_tax_provision(self) -> pd.DataFrame:
        return self.m_ticker.get_financials().loc['TaxProvision']
    
    def get_total_debt(self) -> pd.DataFrame:
        return self.m_ticker.get_balancesheet().loc['TotalDebt']
    
    def get_total_equity(self) -> pd.DataFrame:
        return self.m_ticker.get_balancesheet().loc['TotalEquityGrossMinorityInterest']
