import argparse
import schedule
import time
from db_interface.stock_db_interface import request_access_token, get_stocks
from find_cherries.findCherries import findCherries

# Scheduled time
TIME_SCHEDULE = "09:00"
TIME_ZONE_SCHEDULE = "Europe/Lisbon"

def run(f_args):
    bearer = ''
    if not bearer:
        # Request access token
        respone = request_access_token()
        bearer = respone.json()['access_token']
    stocks = get_stocks(bearer)
    cherry_finder = findCherries(stocks, f_args.sendToDiscord, f_args.safetyMargin, f_args.verbose)
    cherry_finder.find_undervalued_stocks()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Finds undervalued stocks')
    parser.add_argument('--sendToDiscord', required=False, type=bool, default=False, 
                        help='Shall the results be sent to Discord?')
    parser.add_argument('--scheduled', required=False, type=bool, default=False,
                    help="Shall it run once a day?")
    parser.add_argument('--safetyMargin', required=False, type=float, default= 50.0,
                        help="Safety margin above which the stock is considered to be undervalued.")
    parser.add_argument('--verbose', required=False, type=bool, default=False, 
                        help='Shall the results be printed into the terminal?')
    args = parser.parse_args()

    if args.scheduled:
        schedule.every().day.at(TIME_SCHEDULE, TIME_ZONE_SCHEDULE).do(
            run,
            args
        )
        while True:
            schedule.run_pending()
            time.sleep(1)
    else:
        # Run once
        run(args)