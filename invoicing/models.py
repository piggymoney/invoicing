
from __future__ import absolute_import

from sqlalchemy import Column, DateTime, func, Integer, Numeric, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Invoice(Base):
    __tablename__ = 'invoices'

    id = Column(Integer, primary_key=True)
    description = Column(String(200))
    amount = Column(Numeric(precision=10, scale=2))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
