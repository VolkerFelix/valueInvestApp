# In order not to confuse the SQLAlchemy models and the Pydantic models,
# the Pydantic stuff goes in this schemas file.
from typing import Union
from pydantic import BaseModel
from datetime import date

class StockBase(BaseModel):
    m_name: str
    m_description: Union[str, None] = None
    m_intrinsic_value: int
    m_current_market_cap: int
    m_safety_margin: float
    m_undervalued: bool
    m_over_timespan: int
    m_assumed_growth_rate_anual: float

class StockCreate(StockBase):
    pass

class Stock(StockBase):
    m_id: int
    m_last_update: Union[date, None] = None

    class Config:
        orm_mode = True

class User(BaseModel):
    username: str
    email: Union[str ,None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None
    read_stock: Union[bool, None] = None
    write_stock: Union[bool, None] = None

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None