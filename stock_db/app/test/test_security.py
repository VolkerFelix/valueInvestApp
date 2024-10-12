import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from passlib.context import CryptContext
from security import verify_password

PLAIN_PW = os.getenv('REST_API_PASSWORD')
PW_HASHED = os.getenv('REST_API_PASSWORD_HASHED')

def test_verify_pw():
    assert verify_password(PLAIN_PW, PW_HASHED)
