from stock_db_interface import rquest_access_token, get_stocks
from pprint import pprint

if __name__ == '__main__':
    bearer = ''
    if not bearer:
        # Request access token
        respone = rquest_access_token()
        bearer = respone.json()['access_token']
    stocks = get_stocks(bearer)

    pprint(stocks)