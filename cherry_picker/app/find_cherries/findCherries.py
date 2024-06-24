import os
from typing import List
from db_interface.stock_db_interface import StockDBFormat
from discord_interface.discordHook import DiscordHook

WEBHOOKS_CONFIG = {
    "SP500": os.getenv('SP500_WEBHOOK'),
    "DAX": os.getenv('DAX_WEBHOOK')
}

class findCherries:
    def __init__(
            self,
            f_all_stocks: List[StockDBFormat],
            f_send_to_discord: bool,
            f_safety_margin: float,
            f_verbose: bool,
    ):
        self.m_all_stocks = f_all_stocks
        self.m_send_to_discord = f_send_to_discord
        self.m_safety_margin = f_safety_margin
        self.m_verbose = f_verbose
        if self.m_send_to_discord:
            self.m_discord_webhooks = {}
            self.__create_webhooks()

    def __create_webhooks(self):
        for index, webhook_url in WEBHOOKS_CONFIG.items():
            if webhook_url:
                self.m_discord_webhooks[index] = DiscordHook(webhook_url)

    def __notify(self, f_stock: StockDBFormat):
        try:
            self.m_discord_webhooks[f_stock.m_part_of_index].send_message(
                f_message=f_stock.model_dump_json(indent=4),
                f_title=f_stock.m_name
        )
        except KeyError as error:
            print(error)
            print("No webhook for this index.")
            # TODO: Add logging here

    def find_undervalued_stocks(self):
        stock_counter = 0
        for stock in self.m_all_stocks:
            if self.m_verbose:
                print(f"Analysing stock {stock.m_name}")
                print(stock_counter)
                stock_counter += 1
            if stock.m_undervalued == True:
                if stock.m_safety_margin > self.m_safety_margin:
                    if self.m_send_to_discord:
                        self.__notify(stock)
                    if self.m_verbose:
                        print("Cherry found!!")
