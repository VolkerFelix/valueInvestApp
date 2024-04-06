import requests, os
from typing import Union
from pydantic import BaseModel

BASE_URL = os.getenv('STOCK_DB_URL', default="stock_db")
PORT = os.getenv('STOCK_DB_PORT', default='8000')

BASE_URL = "http://" + BASE_URL + ":" + PORT

# Local testing
#BASE_URL = "http://127.0.0.1:8000"

class StockDBFormat(BaseModel):
    m_name: str
    m_description: Union[str, None] = None
    m_intrinsic_value: int
    m_current_market_cap: int
    m_safety_margin: float
    m_undervalued: bool
    m_over_timespan: int
    m_used_growth_rate_annual: float
    m_assumed_growth_rate_company_annual: float

def create_new_stock(f_stock: StockDBFormat, f_bearer_token: str) -> int:
    create_stock_url = BASE_URL + "/stocks/"
    headers = {
        "Authorization": "Bearer " + f_bearer_token
    }
    result = requests.post(url=create_stock_url, data=f_stock.model_dump_json(), headers=headers)
    return result.status_code

def request_access_token():
    token_endpoint = BASE_URL + "/token"
    result = requests.post(
        url=token_endpoint,
        data={
            "grant_type": "password",
            "username": "crawler_client",
            "password": "secret"
        }
    )
    if result.status_code != 200:
        raise requests.exceptions.RequestException(response=result)
    return result