from passlib.context import CryptContext
from typing import Union
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from jose import jwt

from schemas import User

# Secret key to sign the JWT tokens
# Generate new one with 'openssl rand -hex 32'
SECRET_KEY = "997311bc0c2c78080b421ed50e783e4fe3a24952c0c657576eab4052f5add4e3"
# Algo used to sign the tokens
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3600

authenticated_users_db = {
    "crawler_client": {
        "username": "crawler_client",
        "email": "",
        "full_name": "",
        "hashed_password": "$2b$12$JU3IL8o5PCKgMZV9QkaOB.kDXjmHnvaSB1nSJ8DC1S1SK38GKL4Pi",
        "disabled": False,
        "read_stock": True,
        "write_stock": True
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
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def check_read_permission(f_user: User):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User not allowed to read stocks",
        headers={"WWW-Authenticate": "Bearer"}
    )
    if not f_user.read_stock:
        raise credentials_exception
    
def check_write_permission(f_user: User):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User not allowed to write stocks",
        headers={"WWW-Authenticate": "Bearer"}
    )
    if not f_user.write_stock:
        raise credentials_exception
