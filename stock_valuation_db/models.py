from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Float
from sqlalchemy.orm import relationship

from .database import Base

class Stock(Base):
    __tablename__ = "stocks"

    m_id = Column(Integer, unique=True, primary_key=True)
    m_name = Column(String, unique=True, index=True)
    m_last_update = Column(Date)
    m_description = Column(String)
    m_intrinsic_value = Column(Float)
    m_over_timespan_years = Column(Integer)
    m_safety_margin_ratio = Column(Float)
    m_assumed_growth_rate_anual = Column(Float)
