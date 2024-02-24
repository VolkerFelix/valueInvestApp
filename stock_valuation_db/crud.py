from sqlalchemy.orm import Session
from . import models, schemas
from datetime import date

def get_stock(f_db: Session, f_stock_id: int):
    return f_db.query(models.Stock).filter(models.Stock.m_id == f_stock_id).first()

def get_stock_by_name(f_db: Session, f_name: str):
    return f_db.query(models.Stock).filter(models.Stock.m_name == f_name).first()

def get_stocks(f_db: Session, f_skip: int = 0, f_limit: int = 100):
    return f_db.query(models.Stock).offset(f_skip).limit(f_limit).all()

def add_stock(f_db: Session, f_stock: schemas.StockCreate):
    db_stock = models.Stock(**f_stock.model_dump())
    db_stock.m_last_update = date.today()
    f_db.add(db_stock)
    f_db.commit()
    f_db.refresh(db_stock)
    return db_stock