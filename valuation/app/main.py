from db_interface.stock_db_interface import rquest_access_token, create_new_stock
from intrinsic_value.intrinsicValue import IntrinsicValue
from db_interface.stock_db_interface import StockDBFormat
from web_scrape.companiesList import CompaniesList
from web_scrape.forecast import Analysis
from typing import List
from decimal import *
import argparse
import pprint
import warnings

# Time span in years for valuation
TIME_SPAN = 5

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

    return stock

def run_based_on_index_name(
        f_index_name: str,
        f_verbose: bool,
        f_bearer_token: str = ''
    ):
    stock_counter = 0
    for stock_name, symbol in CompaniesList(f_index_name).m_companies.items():
        stock = run_analysis(symbol, stock_name)
        stock_counter += 1
        if f_verbose:
            pprint.pprint(stock)
            print(stock_counter)
        if f_bearer_token:
            add_to_db(stock, f_bearer_token)

def run_based_on_stock_symbol(
        f_stock_symbol: str,
        f_verbose: bool,
        f_bearer_token: str = ''
    ):
    stock = run_analysis(f_stock_symbol)
    if f_verbose:
        pprint.pprint(stock)
    if f_bearer_token:
        add_to_db(stock, f_bearer_token)

def add_to_db(f_stock: dict, f_bearer_token: str) -> int:
    status_code = create_new_stock(StockDBFormat(**f_stock), f_bearer_token)
    if status_code != 200:
        warnings.warn("Could not be stored in DB!")

if __name__ == '__main__':
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
    args = parser.parse_args()

    bearer = ''
    if args.addToDatabase:
        # Request access token
        respone = rquest_access_token()
        print(respone.json())
        bearer = respone.json()['access_token']

    if args.indexName:
        run_based_on_index_name(args.indexName, args.verbose, bearer)
    elif args.stockSymbol:
        run_based_on_stock_symbol(args.stockSymbol, args.verbose, bearer)
    else:
        assert False, "Neither index nor stock defined."
