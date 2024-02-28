from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy.orm import relationship

from database import Base

class Stock(Base):
    __tablename__ = "stocks"

    m_id = Column(Integer, unique=True, primary_key=True)
    m_name = Column(String, unique=True, index=True)
    m_last_update = Column(Date)
    m_description = Column(String)
    m_intrinsic_value = Column(name='Intrinsic value in B$', type_=Float)
    m_intrinsic_value_with_safety = Column(name='Intrinsic value with safety margin in B$', type_=Float)
    m_current_market_cap = Column(name='Current market cap in B$', type_=Float)
    m_diff_intr_val_w_safty_to_m_cap = Column(name='Difference intrinsic value incl. safety / market cap in %', type_=Float)
    m_over_timespan = Column(name='Timespan in years', type_=Integer)
    m_safety_margin_ratio = Column(name='Safety margin in %', type_=Float)
    m_assumed_growth_rate_anual = Column(name='Assumed growth rate in %', type_=Float)
