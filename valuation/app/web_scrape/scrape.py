from bs4 import BeautifulSoup, ResultSet
import requests

S_AND_P_500_URL = "https://stockanalysis.com/list/sp-500-stocks/"

THOUSAND = 1000
MILLION = THOUSAND * 1000
BILLION = MILLION * 1000
TRILLION = BILLION * 1000

# Simulate browser
HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0'
}

def scrape_table(f_url: str, f_table_id: str = '') -> ResultSet:
    response = requests.get(f_url, headers=HEADER)
    if response.history:
        for resp in response.history:
            print(resp.status_code, resp.url)
        print("Final destination:")
        print(response.status_code, response.url)
    soup = BeautifulSoup(response.text, 'html.parser')
    if f_table_id:
        return soup.find_all("table", {"id": f_table_id})
    else:
        return soup.find_all("table")
    
def scrape_div_by_title(f_url: str, f_title: str) -> ResultSet:
    response = requests.get(f_url, headers=HEADER)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.find_all("div", {"title": f_title})

def string_to_float(f_value: str, f_scale: float = 1.0) -> float:
        value_f = 0.0
        if "T" in f_value:
            value_f = float(f_value.replace('T','')) * TRILLION
        elif "B" in f_value: 
            value_f = float(f_value.replace('B','')) * BILLION
        elif "M" in f_value: 
            value_f = float(f_value.replace('M','')) * MILLION
        elif "," in f_value: 
            value_f = float(f_value.replace(',',''))
        elif "N/A" in f_value: 
            value_f = 0.0
        elif "%" in f_value: 
            value_f = float(f_value.replace('%','')) / 100.0

        return value_f * f_scale