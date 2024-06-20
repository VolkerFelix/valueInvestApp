import os
from db_interface.stock_db_interface import request_access_token, get_stocks
from find_cherries.findCherries import findCherries

SP500_WEBHOOK = os.getenv('SP500_WEBHOOK')
DAX_WEBHOOK = os.getenv('DAX_WEBHOOK')

if __name__ == '__main__':
    bearer = ''
    if not bearer:
        # Request access token
        respone = request_access_token()
        bearer = respone.json()['access_token']
    stocks = get_stocks(bearer)
    cherry_finder = findCherries(stocks, SP500_WEBHOOK)
    cherry_finder.find_undervalued_stocks()