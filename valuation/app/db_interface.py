import requests, json, os

BASE_URL = os.getenv('STOCK_DB_URL')
PORT = os.getenv('STOCK_DB_PORT')

BASE_URL = "http://" + BASE_URL + ":" + PORT

def create_new_stock(f_stock: dict, f_bearer_token: str) -> int:
    create_stock_url = BASE_URL + "/stocks/"
    headers = {
        "Authorization": "Bearer " + f_bearer_token
    }
    result = requests.post(url=create_stock_url, data=json.dumps(f_stock), headers=headers)
    return result.status_code

def rquest_access_token():
    token_endpoint = BASE_URL + "/token"
    result = requests.post(
        url=token_endpoint,
        data={
            "grant_type": "password",
            "username": "crawler_client",
            "password": "secret"
        }
    )
    return result