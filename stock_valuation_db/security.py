from passlib.context import CryptContext
from typing import Union
from datetime import datetime, timedelta, timezone
from jose import jwt
import pprint

# Secret key to sign the JWT tokens
# Generate new one with 'openssl rand -hex 32'
SECRET_KEY = "997311bc0c2c78080b421ed50e783e4fe3a24952c0c657576eab4052f5add4e3"
# Algo used to sign the tokens
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

authenticated_users_db = {
    "crawler_client": {
        "username": "crawler_client",
        "email": "",
        "full_name": "",
        "hashed_password": "$2b$12$JU3IL8o5PCKgMZV9QkaOB.kDXjmHnvaSB1nSJ8DC1S1SK38GKL4Pi",
        "disabled": False
    }
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(f_plain_password: str, f_hashed_password: str) -> bool:
    return pwd_context.verify(f_plain_password, f_hashed_password)

def get_password_hashed(f_password: str) -> str:
    return pwd_context.hash(f_password)

def create_access_token(f_data: dict, f_expires_delta: Union[timedelta, None] = None) -> str:
    to_encode = f_data.copy()
    if f_expires_delta:
        expire = datetime.now(timezone.utc) + f_expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    print("Token to be encoded:")
    pprint.pprint(to_encode)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
