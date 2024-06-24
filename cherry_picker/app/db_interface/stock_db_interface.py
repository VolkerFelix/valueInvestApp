import requests, os
from typing import Union, List
from pydantic import BaseModel, TypeAdapter

BASE_URL = os.getenv('STOCK_DB_URL', default="stock_db")
PORT = os.getenv('STOCK_DB_PORT', default='8000')
BASE_URL = "http://" + BASE_URL + ":" + PORT
# Uncomment for local testing
#BASE_URL = "http://localhost:8008"

REST_API_USER = os.getenv('REST_API_USER')
REST_API_PASSWORD = os.getenv('REST_API_PASSWORD')

class StockDBFormat(BaseModel):
    m_name: str
    m_part_of_index: str
    m_description: Union[str, None] = None
    m_intrinsic_value: int
    m_current_market_cap: int
    m_safety_margin: float
    m_undervalued: bool
    m_over_timespan: int
    m_used_growth_rate_annual: float
    m_assumed_growth_rate_company_annual: float

ta = TypeAdapter(List[StockDBFormat])

def get_stocks(f_bearer_token: str) -> List[StockDBFormat]:
    get_stocks_url = BASE_URL + "/stocks/"
    headers = {
        "Authorization": "Bearer " + f_bearer_token
    }
    result = requests.get(
        url=get_stocks_url,
        params={"f_skip": 0, "f_limit": 1000},
        headers=headers
    )
    parsed = ta.validate_python(result.json())
    return parsed

def request_access_token():
    token_endpoint = BASE_URL + "/token"
    result = requests.post(
        url=token_endpoint,
        data={
            "grant_type": "password",
            "username": REST_API_USER,
            "password": REST_API_PASSWORD
        }
    )
    return result