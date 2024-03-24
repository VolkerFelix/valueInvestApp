from typing import List
from db_interface.stock_db_interface import StockDBFormat

class findCherries:
    def __init__(self, f_all_stocks: List[StockDBFormat]):
        self.m_all_stocks = f_all_stocks
        self.m_undervalued = []

    def find_undervalued_stocks(self):
        for stock in self.m_all_stocks:
            print(stock.m_name)
            if stock.m_undervalued == True:
                if stock.m_safety_margin > 50.0:
                    self.m_undervalued.append(stock)
                    print("Cherry found")
