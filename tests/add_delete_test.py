import sys
from pathlib import Path

sys.path.append(str(Path(__file__).absolute().parents[1]))

from app.db import connection, models, _enums
from sqlalchemy.ext.asyncio import AsyncSession
import decimal
import asyncio
from datetime import datetime


async def run_db_add_operation(session: AsyncSession, d_obj: dict):
    obj_type = d_obj.get('T')
    if not obj_type:
        raise
    obj = obj_type(**(d_obj.get('kw')))
    session.add(obj)
    await session.commit()


async def run_db_delete_operation(session: AsyncSession, d_obj: dict):
    obj_type = d_obj.get('T')
    if not obj_type:
        raise
    obj = await session.get(obj_type, d_obj.get('kw').get('id'))
    if not obj:
        raise
    await session.delete(obj)
    await session.commit()


@connection.connection
async def run_db_test(session: AsyncSession, objs: list[object]):
    # creating objects
    for obj in objs:
        await run_db_add_operation(session, obj)
    # deleting objects
    for obj in objs[::-1]:
        await run_db_delete_operation(session, obj)


async def add_delete_test():
    try:
        dt = datetime.now()
        print(f'Test started at {dt}')

        # Create user
        u = {
            'kw': {
                'id': 1,
                'name': 'test_name',
                'email': 'test_email',
                'password': 'test_password'
            },
            'T': models.User
        }
        # Create card
        c = {
            'kw': {
                'id': 1,
                'card_number': 'test_card_number',
                'card_name': 'test_card_name',
                'card_description': 'test_card_description',
                'user_id': 1,
            },
            'T': models.BankCard
        }
        # Create transaction category
        tc = {
            'kw': {
                'id': 1,
                'name': 'test_category',
                'desription': 'test_category',
                'user_id': 1,
            },
            'T': models.TransactionCategory
        }
        # Create financial group
        fc = {
            'kw': {
                'id': 1,
                'status': _enums.FinancialGroupStatusesEnum.OPEN,
                'sum': decimal.Decimal(1),
                'name': 'test_name',
                'description': 'test_description',
                'deadline': dt,
                'user_id': 1,
            },
            'T': models.FinancialGroup
        }
        # Create transaction
        t = {
            'kw': {
                'id': 1,
                'trans_datetime': dt,
                'trans_sum': decimal.Decimal(1),
                'description': 'test_description',
                'target': 1,
                'target_type': _enums.FinancialTypesEnum.GOAL,
                'category_id': 1,
                'bank_card_id': 1,
                'financial_group_id': 1,
            },
            'T': models.Transaction
        }
    
        objs = [u, c, tc, fc, t]
        
        await run_db_test(objs=objs)

        print(f'add_delete_test was successfully completed. Test duration: {datetime.now() - dt}.')
    except Exception:
        print(print(f'add_delete_test failed. Test duration: {datetime.now() - dt}.'))
        raise


if __name__ == '__main__':
    asyncio.run(add_delete_test())
    