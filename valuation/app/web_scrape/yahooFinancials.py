import pandas as pd
import numpy as np
import yfinance as yf
import math
from web_scrape.yahooAnalysis import Analysis

class YahooFinancialStats:
    def __init__(self, f_symbol: str):
        self.m_ticker = yf.Ticker(f_symbol)
        self.m_yahoo_analysis_growth_rate = Analysis(f_symbol).get_growth_rate_estimate_5_year_avg()

    def get_beta(self) -> float:
        try:
            beta = self.m_ticker.info['beta']
        except KeyError:
            # TODO: Log this event
            beta = 1.0
        assert not math.isnan(beta), "NaN beta!"
        return beta
    
    def get_market_cap(self) -> int:
        try: 
            market_cap = self.m_ticker.info['marketCap']
        except KeyError:
            # TODO: Log this
            market_cap = 0
        assert not math.isnan(market_cap), "NaN market cap!"
        return market_cap
    
    def get_total_cash(self) -> int:
        try:
            total_cash = self.m_ticker.info['totalCash']
        except KeyError:
            # TODO: Log this event
            total_cash = 0
        assert not math.isnan(total_cash), "NaN cash!"
        return total_cash
    
    def get_fcf(self) -> pd.DataFrame:
        free_cash_flow = self.m_ticker.get_cash_flow().loc['FreeCashFlow'].fillna(0)
        assert not free_cash_flow.isnull().values.any(), "Contains NaN!"
        return free_cash_flow
    
    def get_ebt(self) -> pd.DataFrame:
        ebt = self.m_ticker.get_financials().loc['PretaxIncome'].fillna(0)
        assert not ebt.isnull().values.any(), "Contains NaN!"
        return ebt
    
    def get_tax_provision(self) -> pd.DataFrame:
        try:
            tax = self.m_ticker.get_financials().loc['TaxProvision'].fillna(0)
        except KeyError:
            # TODO: Log this event
            tax = pd.Series(0, index=np.arange(4))
        assert not tax.isnull().values.any(), "Contains NaN!"
        return tax
    
    def get_total_debt(self) -> pd.DataFrame:
        try:
            debt = self.m_ticker.get_balancesheet().loc['TotalDebt'].fillna(0)
        except KeyError:
            # TODO: Log this event
            debt = pd.Series(0, index=np.arange(4))
        assert not debt.isnull().values.any(), "Contains NaN!"
        return debt
    
    def get_total_equity(self) -> pd.DataFrame:
        equity = self.m_ticker.get_balancesheet().loc['TotalEquityGrossMinorityInterest'].fillna(0)
        assert not equity.isnull().values.any(), "Contains NaN!"
        return equity
    
    def get_analysis_growth_rate_estimate(self) -> float:
        return self.m_yahoo_analysis_growth_rate
