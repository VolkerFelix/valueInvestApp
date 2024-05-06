from web_scrape.yahooFinancials import YahooFinancialStats

# https://www.wallstreetprep.com/knowledge/wacc/

COST_OF_DEBT = 0.05 # For simplicity 5% since no simple scrape source was found
RISK_FREE_RATE = 0.04 # 4% U.S. 10 year treasury 02/2024
ERP = 0.05 # How much extra return above risk-free? Typical value 5%

def get_wacc(f_company: YahooFinancialStats) -> float:
    """
    Get WACC of a company
    """
    # Tax
    ## Get latest EBT and tax provision
    ebt = f_company.get_ebt()[0]
    tax_provision = f_company.get_tax_provision()[0]
    if ebt > 0.001: # prevent div by 0
        tax_rate = max(tax_provision/ebt, 0.0) # Set to 0 in case of negative tax rate
    else:
        tax_rate = 0.0
    # Latest debt
    total_debt = f_company.get_total_debt()[0]
    # Equity
    ## beta: Company's sensitivity to systematic risk
    beta = f_company.get_beta()
    cost_of_equity = RISK_FREE_RATE + beta * ERP
    ## Latest total assets
    total_equity = f_company.get_total_equity()[0]

    wacc = (COST_OF_DEBT * (1 - tax_rate) * total_debt / (total_debt + total_equity)) \
        + (cost_of_equity * total_equity / (total_debt + total_equity))
    
    return wacc