from typing import List, Iterator, Union
from typing_extensions import Annotated
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from . import crud, models, schemas
from .database import SessionLocal, engine
from datetime import datetime, timedelta, timezone

# Secret key to sign the JWT tokens
# Generate new one with 'openssl rand -hex 32'
SECRET_KEY = "997311bc0c2c78080b421ed50e783e4fe3a24952c0c657576eab4052f5add4e3"
# Algo used to sign the tokens
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

models.Base.metadata.create_all(bind=engine)

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

def verify_password(f_plain_password: str, f_hashed_password: str) -> bool:
    return pwd_context.verify(f_plain_password, f_hashed_password)

def get_password_hashed(f_password: str):
    return pwd_context.hash(f_password)

def get_user(f_dummy_db, user_name:str):
    if user_name in f_dummy_db:
        user_dict = f_dummy_db[user_name]
        return schemas.UserInDB(**user_dict)
    
def authenticate_user(f_fake_db, f_username: str, f_password: str):
    user = get_user(f_fake_db, f_username)
    if not user:
        return False
    if not verify_password(f_password, user.hashed_password):
        return False
    return user

def create_access_token(f_data: dict, f_expires_delta: Union[timedelta, None] = None):
    to_encode = f_data.copy()
    if f_expires_delta:
        expire = datetime.now(timezone.utc) + f_expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(f_token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(f_token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, user_name=token_data.username)
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(
        f_current_user: Annotated[schemas.User, Depends(get_current_user)]
):
    if f_current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return f_current_user

@app.post("/token")
async def login_for_access_token(
    f_form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> schemas.Token:
    user = authenticate_user(fake_users_db, f_username=f_form_data.username, f_password=f_form_data.password)
    if not user:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "Incorrect username or password",
            headers= {"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # More info about "sub" (=subject) here:
    # https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#technical-details-about-the-jwt-subject-sub
    access_token = create_access_token(
        f_data={"sub": user.username}, f_expires_delta= access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")


@app.get("/users/me", response_model=schemas.User)
def read_users_me(f_current_user: Annotated[schemas.User, Depends(get_current_active_user)]):
    return f_current_user

# Dependency
## Create an independent session per request and make sure the connection is closed afterwards.
def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/secure/")
def read_stocks_secure(f_token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": f_token}

@app.post("/stocks/", response_model=schemas.Stock)
def add_stock(f_stock: schemas.StockCreate, f_db: Session = Depends(get_db)):
    db_stock = crud.get_stock_by_name(f_db, f_name=f_stock.m_name)
    if db_stock:
        raise HTTPException(status_code=400, detail="Stock already exists")
    return crud.add_stock(f_db=f_db, f_stock=f_stock)

@app.get("/stocks/", response_model=List[schemas.Stock])
def read_stocks(f_skip: int = 0, f_limit: int = 100, f_db: Session = Depends(get_db)):
    stocks = crud.get_stocks(f_db, f_skip=f_skip, f_limit=f_limit)
    return stocks

@app.get("/stocks/{f_stock_id}", response_model=schemas.Stock)
def read_stock(f_stock_id: int, f_db: Session = Depends(get_db)):
    db_stock = crud.get_stock(f_db, f_stock_id=f_stock_id)
    if db_stock is None:
        raise HTTPException(status_code=404, detail="Stock not found")
    return db_stock