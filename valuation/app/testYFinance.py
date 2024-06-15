import yfinance as yf
import pprint

msft = yf.Ticker("MSFT")

print("Free cashflow")
free_cash_flow = msft.get_cash_flow().loc['FreeCashFlow']
pprint.pprint(free_cash_flow[0])
# WACC
print("EBT")
pprint.pprint(msft.get_financials().loc['PretaxIncome'])
print("Tax provision")
pprint.pprint(msft.get_financials().loc['TaxProvision'])
print("Total debt")
pprint.pprint(msft.get_balancesheet().loc['TotalDebt'])
print("Beta")
pprint.pprint(msft.info['beta'])
print("Total equity")
pprint.pprint(msft.get_balancesheet().loc['TotalEquityGrossMinorityInterest'])
print("Market cap")
pprint.pprint(msft.info['marketCap'])
print("Total cash")
pprint.pprint(msft.info['totalCash'])
print("Revenue growth")
pprint.pprint(msft.info['revenueGrowth'])