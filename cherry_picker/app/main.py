import argparse
from db_interface.stock_db_interface import request_access_token, get_stocks
from find_cherries.findCherries import findCherries

# Scheduled time
TIME_SCHEDULE = "09:55"
TIME_ZONE_SCHEDULE = "Europe/Lisbon"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Finds undervalued stocks')
    parser.add_argument('--sendToDiscord', required=False, type=bool, default=False, 
                        help='Shall the results be sent to Discord?')
    parser.add_argument('--scheduled', required=False, type=bool, default=False,
                    help="Shall it run once a day?")
    parser.add_argument('--verbose', required=False, type=bool, default=False, 
                        help='Shall the results be printed into the terminal?')
    args = parser.parse_args()

    bearer = ''
    if not bearer:
        # Request access token
        respone = request_access_token()
        bearer = respone.json()['access_token']
    stocks = get_stocks(bearer)
    cherry_finder = findCherries(stocks, args.sendToDiscord, args.verbose)
    cherry_finder.find_undervalued_stocks()