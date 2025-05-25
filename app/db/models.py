# SQL models.

"""
How downgrade enums: https://stackoverflow.com/questions/25811017/how-to-delete-an-enum-type-value-in-postgres.
"""

from decimal import *
from datetime import datetime
from typing import Annotated

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
)
from sqlalchemy import ForeignKey, func, text
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
)
import enum


class FinancialTypesEnum(enum.IntEnum):
    GOAL = 0
    CREDIT = 1
    TRANSFER = 2


class FinancialGroupStatusesEnum(enum.StrEnum):
    OPEN = 'Open'
    CLOSE = 'Close'


idx = Annotated[int, mapped_column(primary_key=True, index=True, autoincrement=True)]


class Base(AsyncAttrs, DeclarativeBase):
    created: Mapped[datetime] = mapped_column(server_default=func.now())
    updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


class TransactionCategory(Base):

    __tablename__ = 'transaction_categories'
    
    id: Mapped[idx]
    name: Mapped[str] = mapped_column(unique=True)
    desription: Mapped[str | None]


class FinancialGroup(Base):

    __tablename__ = 'financial_groups'
    
    id: Mapped[idx]

    status: Mapped[FinancialGroupStatusesEnum] = mapped_column(default=FinancialGroupStatusesEnum.OPEN,
                                                               server_default=text("'OPEN'"))
    sum: Mapped[Decimal]
    name: Mapped[str]
    description: Mapped[str | None]
    deadline: Mapped[datetime | None]

    transactions: Mapped[list['Transaction']] = relationship(
        'Transaction',
        back_populates='bank_cards',
        cascade='all, delete-orphan'
    )
    
""" It must be a calculating field.

    current_sum: Decimal
    remaining_sum: Decimal
"""


class Transaction(Base):

    __tablename__ = 'transactions'

    id: Mapped[idx]
    trans_datetime: Mapped[datetime] = mapped_column(server_default=func.now())
    trans_sum: Mapped[Decimal]
    description: Mapped[str | None]
    target: Mapped[int | None]  # `FinancialGroup` or another card if `target_type` is not `None`.
    target_type: Mapped[FinancialTypesEnum | None]
    category_id: Mapped[int | None] = mapped_column(ForeignKey('transaction_categories.id'))
    
    bank_card_id: Mapped[str] = mapped_column(ForeignKey('bank_cards.id'))
    financial_group_id: Mapped[int | None] = mapped_column(ForeignKey('financial_groups.id'))

    bank_card: Mapped['BankCard'] = relationship(
        'BankCard',
        back_populates='transactions'
    )
    financial_group: Mapped['FinancialGroup'] = relationship(
        'FinancialGroup',
        back_populates='transactions'
    )


class User(Base):

    __tablename__ = 'users'

    id: Mapped[idx]
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    bank_card: Mapped['BankCard'] = relationship(
        'BankCard',
        back_populates='users',
        uselist=False,
        lazy='selectin'
    )


class BankCard(Base):

    __tablename__ = 'bank_cards'

    id: Mapped[idx]
    card_number: Mapped[str] = mapped_column(unique=True)
    card_name: Mapped[str | None]
    card_description: Mapped[str | None]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user: Mapped['User'] = relationship(
        'User',
        back_populates='bank_cards'
    )

    transactions: Mapped[list['Transaction']] = relationship(
        'Transaction',
        back_populates='bank_cards',
        cascade='all, delete-orphan'
    )


if __name__ == '__main__':
    pass