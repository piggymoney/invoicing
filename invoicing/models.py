from __future__ import absolute_import

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    func,
    Integer,
    Numeric,
    String,
    text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Invoice(Base):
    __tablename__ = 'invoices'

    PENDING = 1
    PAID = 2

    id = Column(Integer, primary_key=True)
    description = Column(String(200), nullable=False)
    amount = Column(Numeric(precision=10, scale=2), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    status = Column(
        Integer,
        default=PENDING,
        nullable=False,
        server_default=text(str(PENDING)),
    )

    payments = relationship('InvoicePayment', backref="invoice")

    def to_json(self):
        status_text = {
            Invoice.PENDING: "Pending",
            Invoice.PAID: "Paid",
        }

        amount_remaining = self.amount - sum(p.amount for p in self.payments)
        return {
            'id': self.id,
            'description': self.description,
            'amount': self.amount,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'status': status_text.get(self.status, "Unknown"),
            'amount_remaining': amount_remaining,
        }


class InvoicePayment(Base):
    __tablename__ = 'invoice_payments'

    id = Column(Integer, primary_key=True)
    amount = Column(Numeric(precision=10, scale=2))
    payment_date = Column(DateTime, server_default=func.now())
    invoice_id = Column(Integer, ForeignKey(Invoice.id))

    def to_json(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'payment_date': self.payment_date,
            'invoice_id': self.invoice_id,
        }


class WebHook(Base):
    __tablename__ = 'web_hooks'

    id = Column(Integer, primary_key=True)
    url_endpoint = Column(String(200), nullable=False)