from typing import Union, List, Iterator
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
from pydantic import BaseModel

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
## Create an independent session per request and make sure the connection is closed afterwards.
def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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