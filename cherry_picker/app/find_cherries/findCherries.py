from typing import List
from db_interface.stock_db_interface import StockDBFormat
from discord_interface.discordHook import DiscordHook

class findCherries:
    def __init__(self, f_all_stocks: List[StockDBFormat], f_discord_hook: str):
        self.m_all_stocks = f_all_stocks
        self.m_discord_hook = DiscordHook(f_discord_hook)

    def find_undervalued_stocks(self):
        for stock in self.m_all_stocks:
            print(stock.m_name)
            if stock.m_undervalued == True:
                if stock.m_safety_margin > 50.0:
                    self.m_discord_hook.send_message(
                        f_message=stock.model_dump_json(indent=4),
                        f_title=stock.m_name
                    )
                    print("Cherry found")
