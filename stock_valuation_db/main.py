from typing import List, Iterator, Union, cast
from typing_extensions import Annotated
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import timedelta

from . import crud, models, schemas, security
from .database import SessionLocal, engine
#from .security import SECRET_KEY, ALGORITHM, verify_password

models.Base.metadata.create_all(bind=engine)

app = FastAPI()    

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user(f_dummy_db, f_username:str) -> schemas.UserInDB:
    if f_username in f_dummy_db:
        user_dict = f_dummy_db[f_username]
        return schemas.UserInDB(**user_dict)
    
def authenticate_user(f_fake_db, f_username: str, f_password: str) -> Union[bool, schemas.UserInDB]:
    user = get_user(f_fake_db, f_username)
    if not user:
        return False
    if not security.verify_password(f_password, user.hashed_password):
        return False
    return user

def get_current_user(f_token: Annotated[str, Depends(oauth2_scheme)]) -> schemas.UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(f_token, security.SECRET_KEY, algorithms=security.ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(security.authenticated_users_db, f_username=token_data.username)
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
    user = authenticate_user(
        security.authenticated_users_db,
        f_username=f_form_data.username,
        f_password=f_form_data.password
    )
    if not user:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "Incorrect username or password",
            headers= {"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    # More info about "sub" (=subject) here:
    # https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#technical-details-about-the-jwt-subject-sub
    access_token = security.create_access_token(
        f_data={"sub": user.username}, f_expires_delta= access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")

# Create an independent session per request and make sure the connection is closed afterwards.
def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/stocks/", response_model= List[schemas.Stock])
def get_stocks(
    f_current_user: Annotated[schemas.User, Depends(get_current_active_user)],
    f_skip: int = 0,
    f_limit: int = 100,
    f_db: Session = Depends(get_db)
) -> List[schemas.Stock]:
    security.check_read_permission(f_current_user)
    stocks = crud.get_stocks(f_db, f_skip=f_skip, f_limit=f_limit)
    return stocks

@app.post("/stocks/", response_model=schemas.Stock)
def add_stock(
    f_current_user: Annotated[schemas.User, Depends(get_current_active_user)],
    f_stock: schemas.StockCreate,
    f_db: Session = Depends(get_db)
):
    security.check_write_permission(f_current_user)  
    db_stock = crud.get_stock_by_name(f_db, f_stock.m_name)
    if db_stock:
        # Update stock values
        print("Want to call update")
        return crud.update_stock(f_db, db_stock, f_stock)
    else:
        # Create new stock
        return crud.add_stock(f_db, f_stock)

@app.get("/stocks/{f_stock_id}", response_model=schemas.Stock)
def read_stock(
    f_current_user: Annotated[schemas.User, Depends(get_current_active_user)],
    f_stock_id: int,
    f_db: Session = Depends(get_db)
):
    security.check_read_permission(f_current_user)
    db_stock = crud.get_stock(f_db, f_stock_id=f_stock_id)
    if db_stock is None:
        raise HTTPException(status_code=404, detail="Stock not found")
    return db_stock