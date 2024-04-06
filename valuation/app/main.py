from db_interface.stock_db_interface import request_access_token, create_new_stock
from intrinsic_value.intrinsicValue import IntrinsicValue
from db_interface.stock_db_interface import StockDBFormat
from web_scrape.companiesList import CompaniesList
from web_scrape.forecast import Analysis
from typing import List
from decimal import *
import argparse
import pprint
import warnings
import schedule
import time
import logging

# Time span in years for valuation
TIME_SPAN = 5

def get_bearer_token() -> str:
    response = request_access_token()
    logger.info(f"Bearer token request response: {response}")
    return response.json()['access_token']

def run_analysis(f_symbol: str, f_stock_name: str = '') -> dict:
    yahoo_analysis = Analysis(f_symbol)
    growth_rate_yahoo = yahoo_analysis.get_expected_growth_rate_over_5_years_per_annum()
    if not growth_rate_yahoo:
        growth_rate_yahoo = 0.0
    intrinsic_value = IntrinsicValue(f_symbol, growth_rate_yahoo, TIME_SPAN)

    stock = {
        "m_name": f_stock_name,
        "m_description": "",
        "m_intrinsic_value": intrinsic_value.m_intrinsic_value,
        "m_current_market_cap": intrinsic_value.m_market_cap,
        "m_safety_margin": intrinsic_value.m_safety_margin,
        "m_undervalued": intrinsic_value.m_undervalued,
        "m_over_timespan": TIME_SPAN,
        "m_used_growth_rate_annual": growth_rate_yahoo,
        "m_assumed_growth_rate_company_annual": growth_rate_yahoo
    }
    logger.info(stock)

    return stock

def run_based_on_index_name(
        f_index_name: str,
        f_sync_db: bool,
        f_verbose: bool
    ):
    bearer = ''
    if f_sync_db:
        # Request new bearer token
        bearer = get_bearer_token()
    stock_counter = 0
    for stock_name, symbol in CompaniesList(f_index_name).m_companies.items():
        stock = run_analysis(symbol, stock_name)
        stock_counter += 1
        if f_verbose:
            pprint.pprint(stock)
            print(stock_counter)
        if f_sync_db:
            add_to_db(stock, bearer)

def run_based_on_stock_symbol(
        f_stock_symbol: str,
        f_sync_db: bool,
        f_verbose: bool
    ):
    bearer = ''
    if f_sync_db:
        # Request new bearer token
        bearer = get_bearer_token()
    stock = run_analysis(f_stock_symbol)
    if f_verbose:
        pprint.pprint(stock)
    if f_sync_db:
        add_to_db(stock, bearer)

def add_to_db(f_stock: dict, f_bearer_token: str) -> int:
    status_code = create_new_stock(StockDBFormat(**f_stock), f_bearer_token)
    if status_code != 200:
        warnings.warn("Could not be stored in DB!")

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler('valuation.log', 'w', 'utf-8')
    logger.addHandler(handler)
    parser = argparse.ArgumentParser(description='Inrinsic value calculation')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--indexName', type=str,
                        help="Provide index name, e.g. SP500")
    group.add_argument('--stockSymbol', type=str,
                       help="Provide symbol of stock, e.g. NVDA")
    parser.add_argument('--addToDatabase', required=False, type=bool, default= False,
                        help='Shall the results be stored in the database?')
    parser.add_argument('--verbose', required=False, type=bool, default=False, 
                        help='Shall the results be printed into the terminal?')
    parser.add_argument('--scheduled', required=False, type=bool, default=False,
                        help="Shall the valuation run once per week?")
    args = parser.parse_args()
    logger.info(args)

    if args.indexName:
        if args.scheduled:
            schedule.every().day.at("10:22", "Europe/Lisbon").do(
                run_based_on_index_name,
                f_index_name = args.indexName,
                f_sync_db = args.addToDatabase,
                f_verbose = args.verbose
            )
        else:
            # Run only once
            run_based_on_index_name(args.indexName, args.addToDatabase, args.verbose)
    elif args.stockSymbol:
        if args.scheduled:
            schedule.every().day.at("10:22", "Europe/Lisbon").do(
                run_based_on_stock_symbol,
                f_stock_symbol = args.stockSymbol,
                f_sync_db = args.addToDatabase,
                f_verbose = args.verbose
            )
        else:
            # Run only once
            run_based_on_stock_symbol(args.stockSymbol, args.addToDatabase, args.verbose)
    else:
        assert False, "Neither index nor stock defined."

    if args.scheduled:
        while True:
            schedule.run_pending()
            time.sleep(1)
