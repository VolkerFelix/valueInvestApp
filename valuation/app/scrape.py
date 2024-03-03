from bs4 import BeautifulSoup, ResultSet
import requests

S_AND_P_500_URL = "https://stockanalysis.com/list/sp-500-stocks/"

# Simulate browser
HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0'
}

def scrape_table(f_url: str) -> ResultSet:
    response = requests.get(f_url, headers=HEADER)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.find_all("table")

def scrape_div_by_title(f_url: str, f_title: str) -> ResultSet:
    response = requests.get(f_url, headers=HEADER)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.find_all("div", {"title": f_title})