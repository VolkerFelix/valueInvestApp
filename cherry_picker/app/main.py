from db_interface.stock_db_interface import rquest_access_token, get_stocks
from find_cherries.findCherries import findCherries
from pprint import pprint

if __name__ == '__main__':
    bearer = ''
    if not bearer:
        # Request access token
        respone = rquest_access_token()
        bearer = respone.json()['access_token']
    stocks = get_stocks(bearer)
    cherry_finder = findCherries(stocks)
    cherry_finder.find_undervalued_stocks()