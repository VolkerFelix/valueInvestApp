from sqlalchemy.orm import Session
from . import models, schemas
from datetime import date
from typing_extensions import Annotated
from typing import List

def get_stock(f_db: Session, f_stock_id: int) -> models.Stock:
    return f_db.query(models.Stock).filter(models.Stock.m_id == f_stock_id).first()

def get_stock_by_name(f_db: Session, f_name: str) -> models.Stock:
    return f_db.query(models.Stock).filter(models.Stock.m_name == f_name).first()

def get_stocks(f_db: Session, f_skip: int = 0, f_limit: int = 100) -> List[models.Stock]:
    return f_db.query(models.Stock).offset(f_skip).limit(f_limit).all()

def add_stock(f_db: Session, f_stock: schemas.StockCreate) -> models.Stock:
    db_stock = models.Stock(**f_stock.model_dump())
    db_stock.m_last_update = date.today()
    f_db.add(db_stock)
    f_db.commit()
    f_db.refresh(db_stock)
    return db_stock

def update_stock(
        f_db: Session,
        f_stock_current: models.Stock,
        f_stock_update: schemas.StockCreate
) -> models.Stock:
    for key, value in f_stock_update.model_dump().items():
        if key == "m_name":
            continue
        setattr(f_stock_current, key, value) if value else None
    f_stock_current.m_last_update = date.today()
    f_db.commit()
    f_db.refresh(f_stock_current)
    return f_stock_current
