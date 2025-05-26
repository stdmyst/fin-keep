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
    # for obj in objs[::-1]:
    #     await run_db_delete_operation(session, obj)


def create_objs(n: int, dt: datetime):
    # Create user
    u = {
        'kw': {
            'id': n,
            'name': f'{n}_test_name',
            'email': f'{n}_test_email',
            'password': f'{n}_test_password'
        },
        'T': models.User
    }
    # Create card
    c = {
        'kw': {
            'id': n,
            'card_number': f'{n}_test_card_number',
            'card_name': f'{n}_test_card_name',
            'card_description': f'{n}_test_card_description',
            'user_id': n,
        },
        'T': models.BankCard
    }
    # Create transaction category
    tc = {
        'kw': {
            'id': n,
            'name': f'{n}_test_category',
            'desription': f'{n}_test_category',
            'user_id': n,
        },
        'T': models.TransactionCategory
    }
    # Create financial group
    fc = {
        'kw': {
            'id': n,
            'status': _enums.FinancialGroupStatusesEnum.OPEN,
            'sum': decimal.Decimal(n),
            'name': f'{n}_test_name',
            'description': f'{n}_test_description',
            'deadline': dt,
            'user_id': n,
        },
        'T': models.FinancialGroup
    }
    # Create transaction
    t = {
        'kw': {
            'id': n,
            'trans_datetime': dt,
            'trans_sum': decimal.Decimal(n),
            'description': 'test_description',
            'target': n,
            'target_type': _enums.FinancialTypesEnum.GOAL,
            'category_id': n,
            'bank_card_id': n,
            'financial_group_id': n,
        },
        'T': models.Transaction
    }
    
    objs = [u, c, tc, fc, t]

    return objs


async def add_delete_test(n: int):
    try:
        dt = datetime.now()
        print(f'Test started at {dt}')
        
        tasks: list[asyncio.Task] = []
        for i in range(1, n+1):
            objs = create_objs(i, dt)
            tasks.append(asyncio.create_task(run_db_test(objs=objs)))

        await asyncio.gather(*tasks)

        print(f'add_delete_test was successfully completed. Test duration: {datetime.now() - dt}.')
    except Exception:
        print(print(f'add_delete_test failed. Test duration: {datetime.now() - dt}.'))
        raise


if __name__ == '__main__':
    asyncio.run(add_delete_test(1))
    