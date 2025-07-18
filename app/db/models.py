# SQL models.

from decimal import *
from datetime import datetime
from typing import Annotated, Optional

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
from ._enums import FinancialTypesEnum, FinancialGroupStatusesEnum


idx = Annotated[int, mapped_column(primary_key=True, index=True, autoincrement=True)]


class Base(AsyncAttrs, DeclarativeBase):
    created: Mapped[datetime] = mapped_column(server_default=func.now())
    updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


class TransactionCategory(Base):

    __tablename__ = 'transaction_categories'
    
    id: Mapped[idx]
    name: Mapped[str] = mapped_column(unique=True)
    desription: Mapped[str | None]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))

    user: Mapped['User'] = relationship(
        'User',
        back_populates='transaction_categories',
        lazy='selectin'
    )
    transactions: Mapped[list['Transaction'] | None] = relationship(
        'Transaction',
        back_populates='category',
        cascade='all, delete-orphan',
        lazy='selectin'
    )


class FinancialGroup(Base):

    __tablename__ = 'financial_groups'
    
    id: Mapped[idx]

    status: Mapped[FinancialGroupStatusesEnum] = mapped_column(default=FinancialGroupStatusesEnum.OPEN,
                                                               server_default=text("'OPEN'"))
    sum: Mapped[Decimal]
    name: Mapped[str]
    description: Mapped[str | None]
    deadline: Mapped[datetime | None]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    
    user: Mapped['User'] = relationship(
        'User',
        back_populates='financial_groups',
        lazy='selectin'
    )
    transactions: Mapped[list['Transaction'] | None] = relationship(
        'Transaction',
        back_populates='financial_group',
        cascade='all, delete-orphan',
        lazy='selectin'
    )
    
    """ It must be a calculating fields
    
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
    category_id: Mapped[int | None] = mapped_column(ForeignKey('transaction_categories.id', ondelete='SET NULL'))
    
    bank_card_id: Mapped[str] = mapped_column(ForeignKey('bank_cards.id', ondelete='CASCADE'))
    financial_group_id: Mapped[int | None] = mapped_column(ForeignKey('financial_groups.id', ondelete='CASCADE'))
    
    category: Mapped[Optional['TransactionCategory']] = relationship(
        'TransactionCategory',
        back_populates='transactions',
        lazy='selectin'
    )
    bank_card: Mapped['BankCard'] = relationship(
        'BankCard',
        back_populates='transactions',
        lazy='selectin'
    )
    financial_group: Mapped[Optional['FinancialGroup']] = relationship(
        'FinancialGroup',
        back_populates='transactions',
        lazy='selectin'
    )


class User(Base):

    __tablename__ = 'users'

    id: Mapped[idx]
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    bank_cards: Mapped[list['BankCard'] | None] = relationship(
        'BankCard',
        back_populates='user',
        cascade='all, delete-orphan',
        lazy='selectin'
    )
    financial_groups: Mapped[list['FinancialGroup'] | None] = relationship(
        'FinancialGroup',
        back_populates='user',
        cascade='all, delete-orphan',
        lazy='selectin'
    )
    transaction_categories: Mapped[list['TransactionCategory'] | None] = relationship(
        'TransactionCategory',
        back_populates='user',
        cascade='all, delete-orphan',
        lazy='selectin'
    )


class BankCard(Base):

    __tablename__ = 'bank_cards'

    id: Mapped[idx]
    card_number: Mapped[str] = mapped_column(unique=True)
    card_name: Mapped[str | None]
    card_description: Mapped[str | None]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    
    user: Mapped['User'] = relationship(
        'User',
        back_populates='bank_cards',
        lazy='selectin'
    )
    transactions: Mapped[list['Transaction'] | None] = relationship(
        'Transaction',
        back_populates='bank_card',
        cascade='all, delete-orphan',
        lazy='selectin'
    )


if __name__ == '__main__':
    pass
