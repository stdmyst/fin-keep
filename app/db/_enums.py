""" How downgrade enums:
For alembic files: https://stackoverflow.com/questions/25811017/how-to-delete-an-enum-type-value-in-postgres

or use `mapped_column(Enum(..., native_enum=False))` => string represenation in database.
"""

import enum


class FinancialTypesEnum(enum.IntEnum):
    CREDIT = 0
    GOAL = 1
    TRANSFER = 2


class FinancialGroupStatusesEnum(enum.IntEnum):
    CLOSE = 0
    OPEN = 1
    