from sqlalchemy import Column, Integer, String, Date, Float, Boolean
from sqlalchemy.orm import relationship

from database import Base

class Stock(Base):
    __tablename__ = "stocks"

    m_id = Column(Integer, unique=True, primary_key=True)
    m_name = Column(String, unique=True, index=True)
    m_part_of_index = Column(String)
    m_last_update = Column(Date)
    m_description = Column(String)
    m_intrinsic_value = Column(name='Intrinsic value in Million $', type_=Integer)
    m_current_market_cap = Column(name='Current market cap in Million $', type_=Integer)
    m_safety_margin = Column(name='Safety margin in %', type_=Float)
    m_undervalued = Column(name='Undervalued', type_=Boolean)
    m_over_timespan = Column(name='Timespan in years', type_=Integer)
    m_used_growth_rate_annual = Column(name='Used growth rate for calc in %', type_=Float)
    m_assumed_growth_rate_company_annual = Column(name='Assumed growth rate in %', type_=Float)
