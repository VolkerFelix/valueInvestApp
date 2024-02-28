import requests
import pandas as pd
import datetime

# Get all company facts based on CIK
# https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json

# Simulate browser
HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0'
}

BASE_URL = 'https://data.sec.gov/api/xbrl/companyconcept/CIK'

def get_net_cash_records(f_cik: str) -> dict:
    net_cash_url = BASE_URL + f_cik + '/us-gaap/NetCashProvidedByUsedInOperatingActivities.json'
    net_cash_records = requests.get(net_cash_url, headers=HEADER)
    return net_cash_records.json()

def get_op_ex_records(f_cik: str) -> dict:
    op_ex_url = BASE_URL + f_cik + '/us-gaap/OperatingExpenses.json'
    op_ex_url_records = requests.get(op_ex_url, headers=HEADER)
    return op_ex_url_records.json()

def get_long_term_debt_records(f_cik: str) -> dict:
    long_term_debt_url = BASE_URL + f_cik + '/us-gaap/LongTermDebt.json'
    long_term_debt_records = requests.get(long_term_debt_url, headers=HEADER)
    return long_term_debt_records.json()

def get_short_term_debt_records(f_cik: str) -> dict:
    short_term_debt_url = BASE_URL + f_cik + '/us-gaap/DebtCurrent.json'
    short_term_debt_records = requests.get(short_term_debt_url, headers=HEADER)
    return short_term_debt_records.json()

def get_effective_income_tax_records(f_cik: str) -> dict:
    tax_url = BASE_URL + f_cik + '/us-gaap/EffectiveIncomeTaxRateContinuingOperations.json'
    tax_records = requests.get(tax_url, headers=HEADER)
    return tax_records.json()

def get_total_assets_records(f_cik: str) -> dict:
    assets_url = BASE_URL + f_cik + '/us-gaap/Assets.json'
    assets_records = requests.get(assets_url, headers=HEADER)
    return assets_records.json()

def get_total_liabilities_records(f_cik: str) -> dict:
    liabilities_url = BASE_URL + f_cik + '/us-gaap/Liabilities.json'
    liabilities_records = requests.get(liabilities_url, headers=HEADER)
    return liabilities_records.json()

def _get_all_10K_statements_USD(f_all_records: dict) -> pd.DataFrame:
    df = pd.DataFrame(f_all_records['units']['USD'])
    elements_10_K = df[df.form=='10-K']
    return elements_10_K

def _get_all_10K_statements_rate(f_all_records: dict) -> pd.DataFrame:
    df = pd.DataFrame(f_all_records['units']['pure'])
    elements_10_K = df[df.form=='10-K']
    return elements_10_K

def get_anual_10K_statements(f_all_records: dict) -> pd.DataFrame:
    df = pd.DataFrame(f_all_records['units']['USD'])
    elements_10_K = df[(df.form=='10-K') & df.frame]
    anual_pattern = elements_10_K.frame.str.match(r'^[A-Z]{2}[0-9]{4}$')
    anual_elemnts_10_K = elements_10_K[anual_pattern]
    return anual_elemnts_10_K

def _get_latest_filing(f_records: pd.DataFrame) -> datetime:
    return pd.to_datetime(f_records['filed']).max()

def get_latest_value_USD(f_records: dict) -> int:
    statements_10K = _get_all_10K_statements_USD(f_records)
    latest_date = _get_latest_filing(statements_10K)
    statements_10K['filed'] = pd.to_datetime(statements_10K['filed'])
    latest_value = statements_10K[statements_10K.filed == latest_date].iloc[-1]['val']
    return latest_value

def get_latest_value_rate(f_records: dict) -> float:
    statements_10K = _get_all_10K_statements_rate(f_records)
    latest_date = _get_latest_filing(statements_10K)
    statements_10K['filed'] = pd.to_datetime(statements_10K['filed'])
    latest_value = statements_10K[statements_10K.filed == latest_date].iloc[-1]['val']
    return latest_value