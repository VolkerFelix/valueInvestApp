from db_interface.stock_db_interface import rquest_access_token, get_stocks
from find_cherries.findCherries import findCherries

WEBHOOK_URL_PROD = "https://discord.com/api/webhooks/1224779729136255128/ACRhjlv6NED9_H-g6_0oTgWH7EMwt_PObry403HCSjWb5u79PGOcnjfyTli_7GztV4tT"

if __name__ == '__main__':
    bearer = ''
    if not bearer:
        # Request access token
        respone = rquest_access_token()
        bearer = respone.json()['access_token']
    stocks = get_stocks(bearer)
    cherry_finder = findCherries(stocks, WEBHOOK_URL_PROD)
    cherry_finder.find_undervalued_stocks()