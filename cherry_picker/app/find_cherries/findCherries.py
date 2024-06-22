import os
from typing import List
from db_interface.stock_db_interface import StockDBFormat
from discord_interface.discordHook import DiscordHook

SP500_WEBHOOK = os.getenv('SP500_WEBHOOK')
DAX_WEBHOOK = os.getenv('DAX_WEBHOOK')

class findCherries:
    def __init__(
            self,
            f_all_stocks: List[StockDBFormat],
            f_send_to_discord: bool,
            f_verbose: bool,
    ):
        self.m_all_stocks = f_all_stocks
        self.m_send_to_discord = f_send_to_discord
        self.m_verbose = f_verbose
        self.m_discord_hook = DiscordHook(SP500_WEBHOOK)

    def find_undervalued_stocks(self):
        for stock in self.m_all_stocks:
            if self.m_verbose:
                print(f"Analysing stock {stock.m_name}")
            if stock.m_undervalued == True:
                if stock.m_safety_margin > 50.0:
                    if self.m_send_to_discord:
                        self.m_discord_hook.send_message(
                            f_message=stock.model_dump_json(indent=4),
                            f_title=stock.m_name
                        )
                    if self.m_verbose:
                        print("Cherry found!!")
