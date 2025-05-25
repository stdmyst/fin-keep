""" How downgrade enums:
For alembic files: https://stackoverflow.com/questions/25811017/how-to-delete-an-enum-type-value-in-postgres

or use `mapped_column(Enum(..., native_enum=False))` => string represenation in database.
"""

import enum


class FinancialTypesEnum(enum.IntEnum):
    GOAL = 0
    CREDIT = 1
    TRANSFER = 2


class FinancialGroupStatusesEnum(enum.StrEnum):
    OPEN = 'Open'
    CLOSE = 'Close'