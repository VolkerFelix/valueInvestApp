from typing import List, Iterator
from typing_extensions import Annotated
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

app = FastAPI()

def fake_hashed_password(f_password: str):
    return "fakehashed" + f_password

def get_user(f_dummy_db, user_name:str):
    if user_name in f_dummy_db:
        user_dict = f_dummy_db[user_name]
        return schemas.UserInDB(**user_dict)
    

def fake_decode_token(f_token):
    user = get_user(fake_users_db, f_token)
    return user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(f_token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(f_token=f_token)
    if not user:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentification credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user

def get_current_active_user(
        f_current_user: Annotated[schemas.User, Depends(get_current_user)]
):
    if f_current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return f_current_user

@app.post("/token")
async def login(f_form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(f_form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = schemas.UserInDB(**user_dict)
    hashed_password = fake_hashed_password(f_form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/users/me")
def read_users_me(f_current_user: Annotated[schemas.User, Depends(get_current_active_user)]):
    return f_current_user

#TODO: Continue here: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/


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