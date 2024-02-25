import requests
from schemas import StockCreate

BASE_URL = "http://127.0.0.1:8000"

def create_new_stock(f_stock: StockCreate) -> int:
    create_stock_url = BASE_URL + "/stocks/"
    result = requests.post(url=create_stock_url, data=f_stock.model_dump_json())
    return result.status_code

def rquest_access_token():
    token_endpoint = BASE_URL + "/token"
    result = requests.post(
        url=token_endpoint,
        data={
            "grant_type": "password",
            "username": "machine",
            "password": "secret"
        }
    )
    return result

if __name__ == "__main__":
    new_stock = StockCreate(
        m_name="Test Stock 3",
        m_assumed_growth_rate_anual= 0.1,
        m_description= "Random company",
        m_intrinsic_value= 500000000,
        m_over_timespan_years= 5,
        m_safety_margin_ratio= 0.5
    )

    status_code = create_new_stock(new_stock)
    print(status_code)

    # Request access token
    respone = rquest_access_token()
    print(respone.json())
